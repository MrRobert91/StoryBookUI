from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain.messages import SystemMessage, HumanMessage
import re
import json
import logging

from api.core.dependencies import get_user_with_credits
from api.services.user_service import UserProfile, deduct_credit
from api.core import config
from api.celery_tasks.app import celery_app
from api.celery_tasks.tasks import generate_story_task
from api.agents.story_agent import graph

router = APIRouter()
logger = logging.getLogger(__name__)

# --- Pydantic Models ---
class TaleRequest(BaseModel):
    description: str

class TaleAIRequest(BaseModel):
    prompt: str

class StoryRequest(BaseModel):
    topic: str
    # model: str = "dall-e-3"  # Configured in backend

# --- Helper Functions ---
def extract_json(text: str) -> dict | None:
    """Extrae un objeto JSON de un string."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None
    return None

# --- Endpoints ---
@router.post("/generate-story")
async def generate_story(req: TaleRequest):
    """Endpoint de prueba, mantenido por ahora."""
    return {"tale": f"Once upon a time about {req.description}"}

@router.post("/generate-story-ai")
async def generate_story_ai(req: TaleAIRequest):
    """Endpoint público para generar un cuento sin autenticación."""
    if not config.GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not set")

    chat = ChatGroq(groq_api_key=config.GROQ_API_KEY, model="llama-3.3-70b-versatile", temperature=0.7)

    system_prompt = (
        "Eres un experto escritor de cuentos infantiles. "
        "Escribe un cuento original con un título y dividido en capítulos, "
        "cada capítulo debe tener un título y un texto breve. "
        "Devuelve SOLO la respuesta en formato JSON con la estructura: "
        '{"title": "...", "chapters": [{"title": "...", "text": "..."}, ...]}'
    )

    messages = [SystemMessage(content=system_prompt), HumanMessage(content=req.prompt)]
    response = await chat.ainvoke(messages)

    story_json = extract_json(response.content)
    if not story_json:
        raise HTTPException(status_code=500, detail="Failed to extract JSON from the story response.")

    return story_json

@router.post("/generate-story-ai-jwt")
async def generate_story_ai_jwt(req: TaleAIRequest, user: UserProfile = Depends(get_user_with_credits)):
    """Genera un cuento usando Groq y descuenta un crédito."""
    logger.info("Generating story for authenticated user %s", user.id)

    if not config.GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not set")

    chat = ChatGroq(groq_api_key=config.GROQ_API_KEY, model="llama-3.3-70b-versatile", temperature=0.7)

    system_prompt = (
        "Eres un experto escritor de cuentos infantiles. "
        "Escribe un cuento original con un título y dividido en capítulos, "
        "cada capítulo debe tener un título y un texto breve. "
        "Devuelve SOLO la respuesta en formato JSON con la estructura: "
        '{"title": "...", "chapters": [{"title": "...", "text": "..."}, ...]}'
    )

    messages = [SystemMessage(content=system_prompt), HumanMessage(content=req.prompt)]
    response = await chat.ainvoke(messages)

    story_json = extract_json(response.content)
    if not story_json:
        raise HTTPException(status_code=500, detail="Failed to extract JSON from the story response.")

    deduct_credit(user)

    # Aquí podríamos guardar el cuento en la base de datos usando user.client

    return story_json

@router.post("/generate-story-ai-images-jwt")
async def generate_story_ai_images_jwt(req: TaleAIRequest, user: UserProfile = Depends(get_user_with_credits)):
    """Genera un cuento con imágenes usando el workflow de LangGraph."""
    logger.info("Generating story with images for user %s", user.id)

    try:
        result = graph.invoke({
            "messages": [{"role": "user", "content": req.prompt}],
            "user_id": user.id,
            "jwt_token": user.token
        })

        final_output = result.get("final_output")
        if not final_output:
            raise HTTPException(status_code=500, detail="Error generating story with images.")

        deduct_credit(user)
        logger.info("Successfully generated story with images for user %s", user.id)

        return final_output

    except Exception as e:
        logger.exception("Error executing the story generation workflow.")
        raise HTTPException(status_code=500, detail=f"Error generating story: {e}")

@router.post("/generate-story-async")
async def generate_story_async(request: StoryRequest, user: UserProfile = Depends(get_user_with_credits)):
    """Inicia la generación de un cuento de forma asíncrona."""
    logger.info("Enqueuing async story generation task for user %s", user.id)

    try:
        task = generate_story_task.delay(
            topic=request.topic,
            user_id=str(user.id),
            jwt_token=user.token,
            model=None
        )
        return {"task_id": task.id, "status": "processing"}
    except Exception as e:
        logger.error("Error enqueuing task: %s", e, exc_info=True)
        raise HTTPException(status_code=503, detail="Service busy or Redis error.")

# --- Guided Story ---

class GuidedStoryRequest(BaseModel):
    age_group: str
    protagonist: str
    scientific_topic: str
    mission: str
    visual_style: str

from api.prompts.guided_story_prompts import VISUAL_STYLE_PROMPTS, TOPIC_PROMPTS, MISSION_PROMPTS

@router.post("/generate_guided_story_async")
async def generate_guided_story_async(req: GuidedStoryRequest, user: UserProfile = Depends(get_user_with_credits)):
    """
    Endpoint para generar un cuento guiado asíncrono.
    Configura el prompt basado en las opciones seleccionadas y encola la tarea.
    Separa el prompt de la historia de los estilos visuales usando descripciones ricas.
    """
    logger.info(f"Generating guided story for user {user.id} with params: {req}")

    # 1. Parsear el protagonista
    if "," in req.protagonist:
        parts = req.protagonist.split(",", 1)
        protag_name = parts[0].strip()
        protag_desc = parts[1].strip()
    else:
        protag_name = req.protagonist
        protag_desc = "un personaje amable y curioso"

    # 2. Obtener descripciones detalladas de los mappings
    # Si no existe la key, usamos el valor raw como fallback (aunque no debería pasar)
    topic_description = TOPIC_PROMPTS.get(req.scientific_topic, req.scientific_topic)
    mission_description = MISSION_PROMPTS.get(req.mission, req.mission)
    visual_style_description = VISUAL_STYLE_PROMPTS.get(req.visual_style, req.visual_style)

    # 3. Construir el prompt de la historia (SOLO TEXTO)
    story_prompt = (
        f"Eres un experto escritor de cuentos infantiles. Escribe un cuento educativo para niños de {req.age_group} años.\n\n"
        f"DATOS PRINCIPALES:\n"
        f"- Protagonista: {protag_name}.\n"
        f"- Tema Científico: {topic_description}\n"
        f"- Trama/Misión: {mission_description}\n\n"
        f"ESTRUCTURA OBLIGATORIA:\n"
        f"1. Título: Creativo y relacionado con la misión.\n"
        f"2. Capítulos: Divide la historia en 3-5 capítulos cortos.\n"
        f"3. Contenido: El tono debe ser divertido, seguro y fácil de leer. "
        f"Asegúrate de explicar el concepto científico de forma natural dentro de la narrativa.\n"
        f"Devuelve SOLO el JSON con el formato establecido."
    )

    # 4. Construir el contexto visual (SOLO IMAGENES)
    image_style_context = (
        f"CHARACTER DESIGN:\n"
        f"- Name: {protag_name}\n"
        f"- Description: {protag_desc}\n\n"
        f"ARTISTIC DIRECTION (Must follow strictly):\n"
        f"{visual_style_description}\n\n"
        f"TARGET AUDIENCE: Children {req.age_group} years old (keep it age-appropriate, safe, and engaging)."
    )

    logger.info(f"Generated Rich Story Prompt: {story_prompt[:100]}...")

    # 5. Encolar la tarea
    try:
        task = generate_story_task.delay(
            topic=story_prompt,
            user_id=str(user.id),
            jwt_token=user.token,
            model=None,
            image_style_context=image_style_context
        )
        return {"task_id": task.id, "status": "processing"}
    except Exception as e:
        logger.error("Error enqueuing guided task: %s", e, exc_info=True)
        raise HTTPException(status_code=503, detail="Service busy or Redis error.")
