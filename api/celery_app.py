import os
import logging
from celery import Celery
from celery.signals import worker_ready

# Configuración de Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

logger = logging.getLogger(__name__)

celery_app = Celery(
    "story_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@worker_ready.connect
def at_start(sender, **kwargs):
    """Log connection details when worker starts"""
    with sender.app.connection() as conn:
        logger.info(f"Worker connected to Redis at: {REDIS_URL}")
        logger.info(f"Broker connection: {conn.as_uri()}")

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
