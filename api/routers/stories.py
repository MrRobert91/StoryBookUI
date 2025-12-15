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
