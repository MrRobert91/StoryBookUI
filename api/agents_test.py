import json
import re
import logging
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from typing_extensions import TypedDict

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from openai import OpenAI
import os
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END

# Nuevas importaciones para S3/Supabase Storage
import boto3
from botocore.client import Config
import requests
import uuid

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
logger = logging.getLogger(__name__)

# Cargar API keys desde variables de entorno
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise EnvironmentError("OPENAI_API_KEY not found. Set it in your .env file.")

groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise EnvironmentError("GROQ_API_KEY not found. Set it in your .env file.")

client = OpenAI(api_key=openai_key)

# ============================================================================
# SUPABASE S3 STORAGE CONFIGURATION
# ============================================================================
SUPABASE_PROJECT_REF = os.getenv("SUPABASE_PROJECT_REF", "qvzbjollfgllkxxzlsoa")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_S3_ENDPOINT = f"https://{SUPABASE_PROJECT_REF}.storage.supabase.co/storage/v1/s3"
SUPABASE_S3_REGION = "eu-central-1"
STORAGE_BUCKET_NAME = os.getenv("STORAGE_BUCKET_NAME", "cuentee_images")

if not SUPABASE_ANON_KEY:
    raise EnvironmentError("SUPABASE_ANON_KEY not found. Set it in your .env file.")

# Variable global para almacenar el contexto del usuario actual
_current_jwt_token = None
_current_user_id = None
_current_story_id = None

def set_user_context(user_id: str, jwt_token: str, story_id: str = None):
    """Set user context for S3 uploads"""
    global _current_jwt_token, _current_user_id, _current_story_id
    _current_jwt_token = jwt_token
    _current_user_id = user_id
    _current_story_id = story_id or str(uuid.uuid4())
    logger.info(f"User context set: user_id={user_id}, story_id={_current_story_id}")

def get_s3_client():
    """
    Create S3 client authenticated with user's JWT token.
    This respects RLS policies in Supabase Storage.
    """
    if not SUPABASE_ANON_KEY:
        raise EnvironmentError("SUPABASE_ANON_KEY not configured")
    
    if not _current_jwt_token:
        raise EnvironmentError("JWT token not set. Call set_user_context() first.")
    
    logger.info(f"Creating S3 client for user: {_current_user_id}")
    
    return boto3.client(
        's3',
        endpoint_url=SUPABASE_S3_ENDPOINT,
        aws_access_key_id=SUPABASE_PROJECT_REF,
        aws_secret_access_key=SUPABASE_ANON_KEY,
        aws_session_token=_current_jwt_token,  # ✅ JWT del usuario autenticado
        region_name=SUPABASE_S3_REGION,
        config=Config(signature_version='s3v4')
    )

def upload_to_supabase_storage(image_url: str, image_type: str) -> str:
    """
    Download image from URL and upload to Supabase Storage using user's JWT.
    
    Args:
        image_url: URL from OpenAI API
        image_type: 'cover' or 'chapter_N'
    
    Returns:
        Public URL of the uploaded image in Supabase Storage, or original URL if upload fails
    """
    if not image_url:
        logger.warning("Empty image_url provided")
        return ""
    
    if not _current_user_id or not _current_jwt_token:
        logger.error("User context not set. Cannot upload to Supabase.")
        return image_url
    
    try:
        # Download image from OpenAI
        logger.info(f"Downloading image from OpenAI: {image_url[:80]}...")
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        image_data = response.content
        logger.info(f"Image downloaded, size: {len(image_data)} bytes")
        
        # Generate filename: user_id/story_id/image_type_uuid.png
        file_extension = "png"
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{_current_user_id}/{_current_story_id}/{image_type}_{unique_id}.{file_extension}"
        
        logger.info(f"Uploading to Supabase Storage: {STORAGE_BUCKET_NAME}/{filename}")
        
        # Upload to Supabase S3 with user's JWT (RLS applied)
        s3_client = get_s3_client()
        s3_client.put_object(
            Bucket=STORAGE_BUCKET_NAME,
            Key=filename,
            Body=image_data,
            ContentType='image/png'
        )
        
        # Construct public URL
        public_url = f"https://{SUPABASE_PROJECT_REF}.supabase.co/storage/v1/object/public/{STORAGE_BUCKET_NAME}/{filename}"
        
        logger.info(f"✓ Image uploaded to Supabase Storage: {public_url}")
        return public_url
        
    except Exception as e:
        logger.exception(f"Error uploading to Supabase Storage: {e}")
        # Fallback to original URL
        return image_url

# ============================================================================
# SCHEMAS
# ============================================================================
class Chapter(BaseModel):
    title: str = Field(description="Chapter title")
    content: str = Field(description="Chapter content/story text")
    image_url: str | None = Field(default=None, description="URL of chapter illustration")

class Story(BaseModel):
    model_config = {"validate_assignment": True}  #  Permite asignación después de crear
    
    title: str = Field(description="Story title")
    cover_image_url: str | None = Field(default=None, description="URL of cover image")  # Añadido
    chapters: List[Chapter] = Field(description="List of story chapters")

class StoryState(TypedDict):
    messages: list
    story_data: Story | None
    final_output: dict | None
    user_id: str | None
    jwt_token: str | None

# ============================================================================
# IMAGE MODEL CONFIGURATION
# ============================================================================
IMAGE_MODELS = {
    "dalle-3": "dall-e-3",
    "dalle-2": "dall-e-2",
    "gpt-image-1": "gpt-image-1",
    "gpt-image-1-mini": "gpt-image-1-mini",
}
DEFAULT_IMAGE_MODEL = os.getenv("IMAGE_MODEL", "dall-e-3").strip().lower()
SELECTED_IMAGE_MODEL = IMAGE_MODELS.get(DEFAULT_IMAGE_MODEL, "dall-e-3")
logger.info(f"Image model: {SELECTED_IMAGE_MODEL}")


# ============================================================================
# CONFIGURATION
# ============================================================================
DEFAULT_NUM_CHAPTERS = int(os.getenv("NUM_CHAPTERS", "4"))
WORDS_PER_CHAPTER = 350
'''
# Asegura estilo infantil ilustrado (no realista)
CHILD_ILLUSTRATION_SUFFIX = (
    "Child-friendly storybook illustration; whimsical, cartoon style; soft lines and rounded shapes; "
    "bright pastel colors; friendly characters; no photorealistic, no realistic, no camera, no lens, "
    "no photographic terms."
)
'''


# ============================================================================
# IMAGE GENERATION
# ============================================================================
_image_counter = {"cover": 0, "chapter": 0}

def generate_image(prompt: str, model: str = None, image_type: str = "image") -> str:
    """
    Generate image using OpenAI API and upload to Supabase Storage.
    Returns the Supabase Storage URL instead of the temporary OpenAI URL.
    """
    model_name = IMAGE_MODELS.get((model or SELECTED_IMAGE_MODEL).lower(), SELECTED_IMAGE_MODEL)
    logger.info(f"Generating image with {model_name}, prompt length: {len(prompt)}")
    
    try:
        # Preparar parámetros base
        params = {
            "model": model_name,
            "prompt": prompt,
            "size": "1024x1024",
            "n": 1
        }
        
        # Añadir 'quality' solo para gpt-image-1 y gpt-image-1-mini
        if model_name in ["gpt-image-1", "gpt-image-1-mini"]:
            params["quality"] = "low"
            logger.debug(f"Added quality='low' for {model_name}")
        
        # estilo vívido para DALL·E 3 (más ilustrativo que natural)
        if model_name == "dall-e-3":
            params["style"] = "vivid"
        
        # Generar imagen con OpenAI
        response = client.images.generate(**params)
        openai_url = response.data[0].url
        logger.info(f"✓ OpenAI generated image: {openai_url[:80]}...")
        
        # Determinar tipo de imagen para nombrado
        if image_type == "cover":
            storage_type = "cover"
        else:
            _image_counter["chapter"] += 1
            storage_type = f"chapter_{_image_counter['chapter']}"
        
        # Subir a Supabase Storage y obtener URL permanente
        supabase_url = upload_to_supabase_storage(openai_url, storage_type)
        
        return supabase_url
        
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return ""

def make_image_prompt(text: str) -> str:
    """Use LLM to create an image prompt for children's illustrations (non-realistic)."""
    try:
        response = image_llm.invoke([
            {
                "role": "system",
                "content": (
                    "Create a concise image prompt suitable for children's books. "
                    "The result MUST describe an illustration in a whimsical storybook/cartoon style. "
                    "Use bright, pastel colors, soft lines, friendly characters, and magical elements. "
                    "AVOID any scary, violent, dark, or realistic/photorealistic imagery. "
                    "Do not mention cameras, lenses, or photographic terms. "
                    "Return ONLY the prompt text."
                ),
            },
            {"role": "user", "content": f"Story text:\n\n{text[:2000]}"},
        ])
        prompt = response.content.strip() if hasattr(response, "content") else str(response).strip()
        
        
        logger.debug("Child-friendly prompt: %s", prompt[:200])
        return prompt
    except Exception as e:
        logger.error("Error creating image prompt: %s", e)
        base = (text[:500] if text else "A friendly fantasy scene")
        return f"{base}"

# ============================================================================
# AGENTS
# ============================================================================
logger.info("Building story_agent (Groq)...")
story_llm = ChatGroq(
    groq_api_key=groq_key,
    model="llama-3.3-70b-versatile",
    temperature=0.7,
)

story_system_prompt = f"""Generate creative fantasy stories for children with exactly {DEFAULT_NUM_CHAPTERS} chapters.

IMPORTANT GUIDELINES:
- Each chapter must have approximately {WORDS_PER_CHAPTER} words
- Content must be family-friendly and appropriate for children
- Use colorful, imaginative descriptions
- Include positive messages and friendly characters
- Return structured JSON with 'title' and 'chapters' array
- Each chapter must have 'title' and 'content' fields

Example structure:
{{
  "title": "The Dragon's Adventure",
  "chapters": [
    {{"title": "Chapter 1: The Discovery", "content": "Once upon a time..."}},
    {{"title": "Chapter 2: The Journey", "content": "The young dragon..."}},
    {{"title": "Chapter 3: The Challenge", "content": "The dragon faced a challenge..."}},
    {{"title": "Chapter 4: The Triumph", "content": "The dragon triumphed..."}}
  ]
}}"""

story_agent = create_agent(
    model=story_llm,
    tools=[],
    response_format=Story,
    system_prompt=story_system_prompt
)
logger.info(f"story_agent ready (configured for {DEFAULT_NUM_CHAPTERS} chapters, ~{WORDS_PER_CHAPTER} words each)")

logger.info("Building image_llm (Groq)...")
image_llm = ChatGroq(
    groq_api_key=groq_key,
    model="llama-3.3-70b-versatile",
    temperature=0.2,
)
logger.info("image_llm ready")

# ============================================================================
# WORKFLOW NODES
# ============================================================================
def story_generation_node(state: StoryState):
    """Generate story text using Groq LLM"""
    logger.info("Node: story_generation")
    messages = state.get("messages", [])
    
    logger.info(f"Invoking story_agent with messages: {messages}")
    
    result = story_agent.invoke({"messages": messages})
    logger.info("story_agent responded")
    
    # Extract structured Story from result
    story = result.get("structured_response") or result.get("story_data") or result
    if isinstance(story, dict):
        story = Story(**story)
    
    logger.info(f"Story generated: {story.title}, {len(story.chapters)} chapters")
    return {"story_data": story}

def image_generation_node(state: StoryState):
    """Generate images for cover and chapters and upload to Supabase Storage"""
    logger.info("Node: image_generation")
    
    # ✅ Obtener user_id y jwt_token del estado
    user_id = state.get("user_id")
    jwt_token = state.get("jwt_token")
    
    if not user_id or not jwt_token:
        logger.error("user_id or jwt_token not provided in state")
        raise ValueError("user_id and jwt_token are required for image generation")
    
    # Configurar contexto de usuario para S3
    story_id = str(uuid.uuid4())
    set_user_context(user_id, jwt_token, story_id)
    
    # Reset counters
    _image_counter["cover"] = 0
    _image_counter["chapter"] = 0
    
    story = state.get("story_data")
    
    if not story:
        logger.error("No story_data in state")
        return {"final_output": None}
    
    # Cover image
    logger.info("Generating cover image...")
    cover_text = f"Book cover for: {story.title}\n\nChapters: {', '.join(c.title for c in story.chapters)}"
    cover_prompt = make_image_prompt(cover_text)
    story.cover_image_url = generate_image(cover_prompt, image_type="cover")
    logger.info("Cover image URL (Supabase): %s", story.cover_image_url)
    
    # Chapter images
    logger.info(f"Generating {len(story.chapters)} chapter images...")
    for idx, chapter in enumerate(story.chapters, 1):
        logger.info(f"Chapter {idx}: {chapter.title}")
        chapter_text = f"{chapter.title}\n\n{chapter.content[:1500]}"
        chapter_prompt = make_image_prompt(chapter_text)
        chapter.image_url = generate_image(chapter_prompt, image_type="chapter")
        logger.info("Chapter %d image URL (Supabase): %s", idx, chapter.image_url)
    
    final_output = story.model_dump()
    final_output["story_id"] = story_id
    final_output["user_id"] = user_id  # ✅ Incluir para referencia
    
    logger.info("All images generated and uploaded to Supabase Storage")
    return {"final_output": final_output}

# ============================================================================
# WORKFLOW GRAPH
# ============================================================================
logger.info("Building workflow graph...")
workflow = StateGraph(StoryState)

workflow.add_node("generate_story", story_generation_node)
workflow.add_node("generate_images", image_generation_node)

workflow.add_edge(START, "generate_story")
workflow.add_edge("generate_story", "generate_images")
workflow.add_edge("generate_images", END)

graph = workflow.compile()
logger.info("Workflow compiled")

# ============================================================================
# EXECUTION
# ============================================================================
if __name__ == "__main__":
    logger.info("Starting workflow...")
    
    try:
        result = graph.invoke({
            "messages": [{"role": "user", "content": "Write a sci-fi story about dragons in space."}],
            "user_id": "test_user",
            "jwt_token": None  # En test mode usa anon key
        })
        logger.info("Workflow completed")
        
        final_output = result.get("final_output") or result
        
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(final_output, f, ensure_ascii=False, indent=2)
        
        logger.info("Result saved to output.json")
        print("Resultado guardado en output.json")
        
    except Exception as e:
        logger.exception("Error in workflow")
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(None, f)