from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import logging

from api.core.dependencies import get_user_with_credits
from api.services.user_service import UserProfile
from api.celery_tasks.tasks import generate_story_task

router = APIRouter()
logger = logging.getLogger(__name__)

# --- Pydantic Models ---
class StoryRequest(BaseModel):
    topic: str
    num_chapters: int = 3
    visual_style: str | None = None
    language: str | None = "Spanish"

# --- Endpoints ---

@router.post("/generate-story-async")
async def generate_story_async(request: StoryRequest, user: UserProfile = Depends(get_user_with_credits)):
    """Inicia la generación de un cuento de forma asíncrona."""
    logger.info("Enqueuing async story generation task for user %s", user.id)

    # Determine Image Style Context
    image_style_context = None
    if request.visual_style:
         # Import here to avoid circulars if any, though top level is better if possible. 
         # Assuming clean imports.
         from api.prompts.guided_story_prompts import VISUAL_STYLE_PROMPTS
         style_desc = VISUAL_STYLE_PROMPTS.get(request.visual_style, request.visual_style)
         image_style_context = f"ARTISTIC DIRECTION (Must follow strictly):\n{style_desc}"

    try:
        task = generate_story_task.delay(
            topic=request.topic,
            user_id=str(user.id),
            jwt_token=user.token,
            model=None,
            num_chapters=request.num_chapters,
            image_style_context=image_style_context,
            story_type="open",
            metadata={
                "language": request.language,
                "story_length": request.num_chapters,
                "artistic_style": request.visual_style
            }
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
    num_chapters: int

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
        f"2. Capítulos: Divide la historia en {req.num_chapters} capítulos cortos.\n"
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
            image_style_context=image_style_context,
            num_chapters=req.num_chapters,
            story_type="guided",
            metadata={
                "age_group": req.age_group,
                "story_length": req.num_chapters,
                "protagonist_name": protag_name,
                "protagonist_description": protag_desc,
                "scientific": True, # Based on endpoint purpose
                "topic": req.scientific_topic,
                "mission": req.mission,
                "visual_style": req.visual_style
            }
        )
        return {"task_id": task.id, "status": "processing"}
    except Exception as e:
        logger.error("Error enqueuing guided task: %s", e, exc_info=True)
        raise HTTPException(status_code=503, detail="Service busy or Redis error.")
