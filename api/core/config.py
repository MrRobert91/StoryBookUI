import os
import logging
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env para desarrollo local
load_dotenv()

# URL de Redis para Celery y Health Checks
REDIS_URL = os.getenv("REDIS_URL") or "redis://localhost:6379/0"

# Credenciales de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Credenciales y modelo de texto de Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEFAULT_GROQ_MODEL = "openai/gpt-oss-120b"
GROQ_MODEL = os.getenv("GROQ_MODEL", "").strip() or DEFAULT_GROQ_MODEL
# Older deployments may still override the new default with the retired model.
if GROQ_MODEL == "llama-3.3-70b-versatile":
    logging.getLogger(__name__).warning(
        "GROQ_MODEL=llama-3.3-70b-versatile is retired for this deployment; "
        "using %s. Update GROQ_MODEL in both API and worker settings.",
        DEFAULT_GROQ_MODEL,
    )
    GROQ_MODEL = DEFAULT_GROQ_MODEL

DEFAULT_IMAGE_MODEL = "gpt-image-2-2026-04-21"
GPT_IMAGE_MODELS = {
    "gpt-image-1", "gpt-image-1-mini", "gpt-image-1.5",
    "gpt-image-2", "gpt-image-2-2026-04-21",
    "gpt-image-2.5-flare", "gpt-image-2.5-flare-2026-09-08",
    "gpt-image-2.5-sunburst", "gpt-image-2.5-sunburst-2026-09-08",
}
IMAGE_MODELS = {model: model for model in GPT_IMAGE_MODELS}
IMAGE_MODELS.update({
    "dalle-2": "dall-e-2", "dall-e-2": "dall-e-2",
    "dalle-3": "dall-e-3", "dall-e-3": "dall-e-3",
})
_configured_image_model = os.getenv("IMAGE_MODEL", "").strip().lower() or DEFAULT_IMAGE_MODEL
if _configured_image_model not in IMAGE_MODELS:
    raise ValueError(
        f"Unsupported IMAGE_MODEL={_configured_image_model!r}. "
        f"Choose one of: {', '.join(sorted(IMAGE_MODELS))}"
    )
IMAGE_MODEL = IMAGE_MODELS[_configured_image_model]

# Podríamos añadir validaciones aquí para asegurar que las variables críticas estén definidas
# Por ejemplo:
# if not SUPABASE_URL or not SUPABASE_ANON_KEY:
#     raise ValueError("Las variables de entorno de Supabase son obligatorias")
