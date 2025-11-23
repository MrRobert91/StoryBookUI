import os
import logging
from celery import Celery
from celery.signals import worker_ready, after_setup_logger

# Configuración de Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Mask Redis URL for logging
masked_redis_url = REDIS_URL
if "@" in REDIS_URL:
    prefix = REDIS_URL.split("@")[0]
    suffix = REDIS_URL.split("@")[1]
    # Keep protocol, mask password
    if "//" in prefix:
        proto, auth = prefix.split("//")
        if ":" in auth:
            user, _ = auth.split(":")
            masked_redis_url = f"{proto}//{user}:******@{suffix}"
        else:
            masked_redis_url = f"{proto}//******@{suffix}"

logger = logging.getLogger(__name__)

celery_app = Celery(
    "story_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    logger.info(f"Celery configured with Redis URL: {masked_redis_url}")

@worker_ready.connect
def at_start(sender, **kwargs):
    """Log connection details when worker starts"""
    logger.info(f"Worker connected to Redis at: {masked_redis_url}")
    try:
        with sender.app.connection() as conn:
            logger.info(f"Broker connection established: {conn.as_uri()}")
    except Exception as e:
        logger.error(f"Failed to establish initial connection in worker_ready: {e}")

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_pool_limit=1,
    broker_connection_retry_on_startup=True,
    worker_concurrency=1,
    broker_transport_options={"max_connections": 2},
    result_backend_transport_options={"max_connections": 2},
)
