from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import asyncio
import redis
from datetime import datetime, timezone, timedelta

from api.core import config
from api.routers import stories, tasks
from api.services.supabase_client import service_supabase_client

# Configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Creación de la aplicación FastAPI
app = FastAPI(
    title="StoryBook API",
    description="API para la generación de cuentos infantiles personalizados con IA.",
    version="1.0.0"
)

# Configuración del middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, debería ser una lista de orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de los routers
app.include_router(stories.router, prefix="/stories", tags=["Stories"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])


async def refill_plus_credits():
    """
    Tarea en segundo plano que se ejecuta una vez al día para rellenar los créditos
    de los usuarios con plan 'plus'.
    """
    while True:
        if service_supabase_client:
            now = datetime.now(timezone.utc)
            try:
                resp = (
                    service_supabase_client.table("profiles")
                    .select("id, credits, plan, plus_since, last_credited_at")
                    .eq("plan", "plus")
                    .execute()
                )
                for user in resp.data or []:
                    last_credited_str = user.get("last_credited_at") or user.get("plus_since")
                    if last_credited_str:
                        last_dt = datetime.fromisoformat(str(last_credited_str).replace("Z", "+00:00"))
                        if now - last_dt >= timedelta(days=30):
                            new_credits = (user.get("credits") or 0) + 10
                            service_supabase_client.table("profiles").update(
                                {"credits": new_credits, "last_credited_at": now.isoformat()}
                            ).eq("id", user["id"]).execute()
                            logger.info(f"Refilled credits for user {user['id']}.")
            except Exception as e:
                logger.error(f"Error during credit refill task: {e}", exc_info=True)

        # Esperar 24 horas para la siguiente ejecución
        await asyncio.sleep(60 * 60 * 24)

@app.on_event("startup")
async def startup_event():
    """
    Eventos que se ejecutan al iniciar la aplicación.
    """
    # 1. Health Check de Redis
    if config.REDIS_URL:
        try:
            logger.info("Checking Redis connection...")
            r = redis.from_url(config.REDIS_URL)
            r.ping()
            logger.info("✅ Redis connection successful.")
            r.close()
        except Exception as e:
            logger.error(f"❌ Redis connection failed on startup: {e}")
    else:
        logger.warning("⚠️ REDIS_URL not set, Redis health check skipped.")

    # 2. Iniciar la tarea de recarga de créditos en segundo plano
    logger.info("Starting background task for refilling credits.")
    asyncio.create_task(refill_plus_credits())

@app.get("/", tags=["Health Check"])
async def read_root():
    """
    Endpoint raíz para verificar que la API está funcionando.
    """
    return {"status": "ok", "message": "Welcome to the StoryBook API!"}
