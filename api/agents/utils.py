import os
import json
import logging
import base64
import uuid
import requests
import boto3
from typing import List
from botocore.client import Config
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
logger = logging.getLogger(__name__)

# Cargar API keys
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise EnvironmentError("OPENAI_API_KEY not found. Set it in your .env file.")

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
    """Create S3 client authenticated with user's JWT token."""
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
        aws_session_token=_current_jwt_token,  # JWT del usuario autenticado
        region_name=SUPABASE_S3_REGION,
        config=Config(signature_version='s3v4')
    )

def upload_image_bytes_to_supabase(image_data: bytes, image_type: str) -> str:
    """Upload raw image bytes to Supabase Storage."""
    if not _current_user_id or not _current_jwt_token:
        logger.error("User context not set. Cannot upload to Supabase.")
        return ""
    
    try:
        file_extension = "png"
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{_current_user_id}/{_current_story_id}/{image_type}_{unique_id}.{file_extension}"
        
        logger.info(f"Uploading to Supabase Storage: {STORAGE_BUCKET_NAME}/{filename}")
        
        s3_client = get_s3_client()
        s3_client.put_object(
            Bucket=STORAGE_BUCKET_NAME,
            Key=filename,
            Body=image_data,
            ContentType='image/png'
        )
        
        public_url = f"https://{SUPABASE_PROJECT_REF}.supabase.co/storage/v1/object/public/{STORAGE_BUCKET_NAME}/{filename}"
        
        logger.info(f"✓ Image uploaded to Supabase Storage: {public_url}")
        return public_url
        
    except Exception as e:
        logger.exception(f"Error uploading to Supabase Storage: {e}")
        return ""

def upload_to_supabase_storage(image_url: str, image_type: str) -> str:
    """Download image from URL and upload to Supabase Storage using user's JWT."""
    if not image_url:
        logger.warning("Empty image_url provided")
        return ""
    
    try:
        logger.info(f"Downloading image from OpenAI: {image_url[:80]}...")
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        image_data = response.content
        logger.info(f"Image downloaded, size: {len(image_data)} bytes")
        
        public_url = upload_image_bytes_to_supabase(image_data, image_type)
        return public_url if public_url else image_url
        
    except Exception as e:
        logger.exception(f"Error downloading/uploading to Supabase Storage: {e}")
        return image_url

# ============================================================================
# SCHEMAS
# ============================================================================
class Chapter(BaseModel):
    title: str = Field(description="Chapter title")
    content: str = Field(description="Chapter content/story text")
    image_url: str | None = Field(default=None, description="URL of chapter illustration")

class Story(BaseModel):
    model_config = {"validate_assignment": True}
    
    title: str = Field(description="Story title")
    cover_image_url: str | None = Field(default=None, description="URL of cover image")
    chapters: List[Chapter] = Field(description="List of story chapters")

class StoryState(TypedDict):
    messages: list
    story_data: Story | None
    final_output: dict | None
    user_id: str | None
    jwt_token: str | None
    model: str | None
    image_style_context: str | None

# ============================================================================
# IMAGE GENERATION LOGIC
# ============================================================================
IMAGE_MODELS = {
    "dalle-3": "dall-e-3",
    "dalle-2": "dall-e-2",
    "gpt-image-1": "gpt-image-1",
    "gpt-image-1-mini": "gpt-image-1-mini",
    "gpt-image-1.5": "gpt-image-1.5",
}
DEFAULT_IMAGE_MODEL = os.getenv("IMAGE_MODEL", "dall-e-3").strip().lower()
SELECTED_IMAGE_MODEL = IMAGE_MODELS.get(DEFAULT_IMAGE_MODEL, "dall-e-3")
_image_counter = {"cover": 0, "chapter": 0}

def generate_image(prompt: str, model: str = None, image_type: str = "image") -> str:
    """Generate image using OpenAI and upload to Supabase."""
    model_name = IMAGE_MODELS.get((model or SELECTED_IMAGE_MODEL).lower(), SELECTED_IMAGE_MODEL)
    logger.info(f"Generating image with {model_name}, prompt length: {len(prompt)}")
    
    try:
        params = {
            "model": model_name,
            "prompt": prompt,
            "size": "1024x1024",
            "n": 1
        }
        
        is_base64_model = model_name in ["gpt-image-1", "gpt-image-1-mini", "gpt-image-1.5"]
        
        if is_base64_model:
            params["quality"] = "low"
            logger.debug(f"Configured for base64 output ({model_name})")
        
        if model_name == "dall-e-3":
            params["style"] = "vivid"
        
        response = client.images.generate(**params)
        
        # Logging response debug
        try:
            first_item_dict = response.data[0].__dict__.copy() if response.data else {}
            if 'b64_json' in first_item_dict and first_item_dict['b64_json']:
                first_item_dict['b64_json'] = first_item_dict['b64_json'][:100] + "... (truncated)"
            
            logger.info(f" [DEBUG] Raw Image Response for: {model_name}: {first_item_dict if response.data else 'No data'}")
        except:
            pass

        if image_type == "cover":
            storage_type = "cover"
        else:
            _image_counter["chapter"] += 1
            storage_type = f"chapter_{_image_counter['chapter']}"
        
        if is_base64_model:
            first_item = response.data[0]
            b64_data = getattr(first_item, 'b64_json', None)
            
            if not b64_data:
                logger.warning(f"No b64_json in response for {model_name}. Checks if url exists.")
                if hasattr(first_item, 'url') and first_item.url:
                     logger.info("✓ Found URL instead of b64_json, switching method.")
                     return upload_to_supabase_storage(first_item.url, storage_type)
                
                logger.error("No image data (b64 or url) found in response.")
                return ""
            
            logger.info("✓ OpenAI generated image (base64)")
            image_data = base64.b64decode(b64_data)
            return upload_image_bytes_to_supabase(image_data, storage_type)
        else:
            openai_url = response.data[0].url
            logger.info(f"✓ OpenAI generated image: {openai_url[:80]}...")
            return upload_to_supabase_storage(openai_url, storage_type)
            
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return ""
