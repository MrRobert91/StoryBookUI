from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from langchain.messages import SystemMessage, HumanMessage
from supabase import create_client, Client
import os
import re
import json
import asyncio
from datetime import datetime, timezone, timedelta
import logging
from agents_test import graph, StoryState

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Cliente privilegiado para tareas en segundo plano
service_supabase: Client | None = None
if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY:
    service_supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def get_supabase_client(token: str) -> Client:
    """Devuelve un cliente de Supabase autenticado con el JWT del usuario."""
    logger.info("Creando cliente de Supabase para token con prefijo %s", token[:10])
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        logger.error("Supabase no configurado")
        raise HTTPException(status_code=500, detail="Supabase no configurado")
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    try:
        client.postgrest.auth(token)
    except Exception as exc:  # pragma: no cover - network errors
        logger.exception("Error autenticando cliente de Supabase")
        raise HTTPException(status_code=401, detail="Token inválido") from exc
    return client


class TaleRequest(BaseModel):
    description: str


@app.post("/generate-story")
async def generate_story(req: TaleRequest):
    return {"tale": f"Once upon a time about {req.description}"}


class TaleAIRequest(BaseModel):
    prompt: str


@app.post("/generate-story-ai")
async def generate_story_ai(req: TaleAIRequest):
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        return {"error": "GROQ_API_KEY not set"}

    # Crea el modelo de chat Groq
    chat = ChatGroq(
        groq_api_key=groq_api_key, model="llama-3.3-70b-versatile", temperature=0.7
    )

    system_prompt = (
        "Eres un experto escritor de cuentos infantiles. "
        "Escribe un cuento original con un título y dividido en capítulos, "
        "cada capítulo debe tener un título y un texto breve. "
        "Devuelve SOLO la respuesta en formato JSON con la estructura: "
        '{"title": "...", "chapters": [{"title": "...", "text": "..."}, ...]}'
    )

    messages = [SystemMessage(content=system_prompt), HumanMessage(content=req.prompt)]

    response = await chat.ainvoke(messages)

    def extract_json(text):
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                return None
        return None

    story_json = extract_json(response.content)
    if not story_json:
        return {"error": "No se pudo extraer el JSON", "raw": response.content}
    return story_json


def verify_jwt(token: str) -> str:
    """Valida el JWT con Supabase y devuelve el ID de usuario."""
    logger.info("Verificando JWT")
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        logger.error("Supabase no configurado")
        raise HTTPException(status_code=500, detail="Supabase no configurado")
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    try:
        user_resp = client.auth.get_user(token)
    except Exception as exc:  # pragma: no cover - network errors
        logger.exception("Error al verificar JWT con Supabase")
        raise HTTPException(status_code=401, detail="Token inválido") from exc
    if not user_resp or user_resp.user is None:
        logger.warning("Supabase no devolvió usuario para el token")
        raise HTTPException(status_code=401, detail="Token inválido")
    logger.info("JWT válido para el usuario %s", user_resp.user.id)
    return user_resp.user.id


@app.post("/generate-story-ai-jwt")
async def generate_story_ai_jwt(
    req: TaleAIRequest, authorization: str | None = Header(default=None)
):
    logger.info("Solicitud a /generate-story-ai-jwt")
    if not authorization or not authorization.startswith("Bearer "):
        logger.warning("Cabecera Authorization ausente o inválida: %s", authorization)
        raise HTTPException(status_code=401, detail="Falta token de autenticación")
    token = authorization.split(" ", 1)[1]
    user_id = verify_jwt(token)
    logger.info("Usuario autenticado: %s", user_id)

    supabase = get_supabase_client(token)

    user_resp = (
        supabase.table("profiles")
        .select("credits, plan")
        .eq("id", user_id)
        .single()
        .execute()
    )
    data = user_resp.data or {}
    logger.info("Perfil de usuario: %s", data)

    credits = data.get("credits", 0)
    if credits <= 0:
        logger.warning("Usuario %s sin créditos", user_id)
        raise HTTPException(
            status_code=402,
            detail="No tienes créditos disponibles. Suscríbete para continuar.",
        )

    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not set")

    chat = ChatGroq(
        groq_api_key=groq_api_key,
        model="llama-3.3-70b-versatile",
        temperature=0.7,
    )

    system_prompt = (
        "Eres un experto escritor de cuentos infantiles. "
        "Escribe un cuento original con un título y dividido en capítulos, "
        "cada capítulo debe tener un título y un texto breve. "
        "Devuelve SOLO la respuesta en formato JSON con la estructura: "
        '{"title": "...", "chapters": [{"title": "...", "text": "..."}, ...]}'
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=req.prompt),
    ]
    response = await chat.ainvoke(messages)

    def extract_json(text):
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                return None
        return None

    story_json = extract_json(response.content)
    if not story_json:
        raise HTTPException(status_code=500, detail="No se pudo extraer el JSON")

    supabase.table("profiles").update({"credits": credits - 1}).eq(
        "id", user_id
    ).execute()
    # supabase.table("stories").insert(
    #     {
    #         "user_id": user_id,
    #         "title": title,
    #         "content": json.dumps(story_json),
    #         "prompt": req.prompt,
    #     }
    # ).execute()
    return story_json


@app.post("/generate-story-ai-images-jwt")
async def generate_story_ai_images_jwt(
    req: TaleAIRequest, authorization: str | None = Header(default=None)
):
    """
    Endpoint protegido por JWT que genera un cuento con imágenes usando el workflow de agents_test.py
    """
    logger.info("Solicitud a /generate-story-ai-images-jwt")
    
    # Validar JWT
    if not authorization or not authorization.startswith("Bearer "):
        logger.warning("Cabecera Authorization ausente o inválida: %s", authorization)
        raise HTTPException(status_code=401, detail="Falta token de autenticación")
    
    token = authorization.split(" ", 1)[1]
    user_id = verify_jwt(token)
    logger.info("Usuario autenticado: %s", user_id)

    # Verificar créditos
    supabase = get_supabase_client(token)
    user_resp = (
        supabase.table("profiles")
        .select("credits, plan")
        .eq("id", user_id)
        .single()
        .execute()
    )
    data = user_resp.data or {}
    logger.info("Perfil de usuario: %s", data)

    credits = data.get("credits", 0)
    if credits <= 0:
        logger.warning("Usuario %s sin créditos", user_id)
        raise HTTPException(
            status_code=402,
            detail="No tienes créditos disponibles. Suscríbete para continuar.",
        )

    # Generar cuento con imágenes usando el workflow
    try:
        logger.info("Invocando workflow con prompt: %s", req.prompt[:100])
        
        result = graph.invoke({
            "messages": [{"role": "user", "content": req.prompt}]
        })
        
        final_output = result.get("final_output")
        
        if not final_output:
            logger.error("El workflow no devolvió final_output")
            raise HTTPException(
                status_code=500, 
                detail="Error generando el cuento con imágenes"
            )
        
        logger.info("Cuento generado exitosamente: %s", final_output.get("title"))
        
        # Descontar crédito
        supabase.table("profiles").update({"credits": credits - 1}).eq(
            "id", user_id
        ).execute()
        logger.info("Crédito descontado. Créditos restantes: %d", credits - 1)
        
        # Opcional: Guardar el cuento en la base de datos
        try:
            supabase.table("stories").insert(
                {
                    "user_id": user_id,
                    "title": final_output.get("title", "Sin título"),
                    "content": json.dumps(final_output),
                    "prompt": req.prompt,
                }
            ).execute()
            logger.info("Cuento guardado en la base de datos")
        except Exception as e:
            logger.warning("No se pudo guardar el cuento en la BD: %s", e)
        
        return final_output
        
    except Exception as e:
        logger.exception("Error ejecutando el workflow")
        raise HTTPException(
            status_code=500,
            detail=f"Error generando el cuento: {str(e)}"
        )


async def refill_plus_credits():
    while True:
        if service_supabase is not None:
            now = datetime.now(timezone.utc)
            resp = (
                service_supabase.table("profiles")
                .select("id, credits, plan, plus_since, last_credited_at")
                .eq("plan", "plus")
                .execute()
            )
            for user in resp.data or []:
                last = user.get("last_credited_at") or user.get("plus_since")
                if last:
                    last_dt = datetime.fromisoformat(str(last).replace("Z", "+00:00"))
                else:
                    last_dt = now
                if now - last_dt >= timedelta(days=30):
                    new_credits = (user.get("credits") or 0) + 10
                    service_supabase.table("profiles").update(
                        {"credits": new_credits, "last_credited_at": now.isoformat()}
                    ).eq("id", user["id"]).execute()
        await asyncio.sleep(60 * 60 * 24)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(refill_plus_credits())
