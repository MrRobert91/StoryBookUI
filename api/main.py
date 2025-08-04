from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from supabase import create_client, Client
import jwt
import os
import re
import json
import asyncio
from datetime import datetime, timezone, timedelta

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de Supabase y JWT
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

# Cliente privilegiado para tareas en segundo plano
service_supabase: Client | None = None
if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY:
    service_supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def get_supabase_client(token: str) -> Client:
    """Devuelve un cliente de Supabase autenticado con el JWT del usuario."""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise HTTPException(status_code=500, detail="Supabase no configurado")
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    client.postgrest.auth(token)
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
    chat = ChatGroq(groq_api_key=groq_api_key, model="llama-3.3-70b-versatile", temperature=0.7)

    system_prompt = (
        "Eres un experto escritor de cuentos infantiles. "
        "Escribe un cuento original dividido en capítulos, "
        "cada capítulo debe tener un título y un texto breve. "
        "Devuelve SOLO la respuesta en formato JSON con la estructura: "
        "{\"chapters\": [{\"title\": \"...\", \"text\": \"...\"}, ...]}"
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=req.prompt)
    ]

    response = chat(messages)

    def extract_json(text):
        match = re.search(r'\{.*\}', text, re.DOTALL)
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
    if not SUPABASE_JWT_SECRET:
        raise HTTPException(status_code=500, detail="SUPABASE_JWT_SECRET not set")
    try:
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


@app.post("/generate-story-ai-jwt")
async def generate_story_ai_jwt(
    req: TaleAIRequest, authorization: str | None = Header(default=None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Falta token de autenticación")
    token = authorization.split(" ", 1)[1]
    user_id = verify_jwt(token)

    supabase = get_supabase_client(token)

    user_resp = (
        supabase.table("profiles")
        .select("credits, plan")
        .eq("id", user_id)
        .single()
        .execute()
    )
    data = user_resp.data or {}

    credits = data.get("credits", 0)
    if credits <= 0:
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
        "Escribe un cuento original dividido en capítulos, "
        "cada capítulo debe tener un título y un texto breve. "
        "Devuelve SOLO la respuesta en formato JSON con la estructura: "
        "{\"chapters\": [{\"title\": \"...\", \"text\": \"...\"}, ...]}"
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=req.prompt),
    ]
    response = chat(messages)

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

    supabase.table("profiles").update({"credits": credits - 1}).eq("id", user_id).execute()
    title = (
        story_json.get("chapters", [{}])[0].get("title")
        if story_json.get("chapters")
        else "Story"
    )
    supabase.table("stories").insert(
        {
            "user_id": user_id,
            "title": title,
            "content": json.dumps(story_json),
            "prompt": req.prompt,
        }
    ).execute()
    return story_json


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
