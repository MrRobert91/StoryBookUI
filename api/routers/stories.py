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
    lang: str | None = "en"

# --- Endpoints ---

@router.post("/generate-story-async")
async def generate_story_async(request: StoryRequest, user: UserProfile = Depends(get_user_with_credits)):
    """Inicia la generación de un cuento de forma asíncrona."""
    logger.info("Enqueuing async story generation task for user %s", user.id)

    # Determine Image Style Context
    image_style_context = None
    if request.visual_style:
         from api.prompts.utils import get_localized_prompts
         prompts = get_localized_prompts(request.lang or "en")
         style_desc = prompts["VISUAL_STYLE_PROMPTS"].get(request.visual_style, request.visual_style)
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
                "language": request.lang,
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
    lang: str = "en"

from api.prompts.utils import get_localized_prompts

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

    # 2. Obtener prompts localizados usando la lógica centralizada
    from api.prompts.guided_story_prompts import get_guided_story_prompts
    
    guided_prompts = get_guided_story_prompts(
        lang=req.lang,
        age_group=req.age_group,
        protagonist_name=protag_name,
        protagonist_desc=protag_desc,
        scientific_topic=req.scientific_topic,
        mission=req.mission,
        visual_style=req.visual_style,
        num_chapters=req.num_chapters
    )
    
    story_prompt = guided_prompts["story_prompt"]
    image_style_context = guided_prompts["image_style_context"]

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
                "visual_style": req.visual_style,
                "language": req.lang
            }
        )
        return {"task_id": task.id, "status": "processing"}
    except Exception as e:
        logger.error("Error enqueuing guided task: %s", e, exc_info=True)
        raise HTTPException(status_code=503, detail="Service busy or Redis error.")
