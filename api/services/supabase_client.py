from supabase import create_client, Client
from fastapi import HTTPException
import logging

from api.core import config

logger = logging.getLogger(__name__)

def get_supabase_service_client() -> Client:
    """
    Devuelve un cliente de Supabase privilegiado (rol de servicio).
    Es seguro usar este cliente en el lado del servidor para tareas administrativas.
    """
    if not config.SUPABASE_URL or not config.SUPABASE_SERVICE_ROLE_KEY:
        logger.error("Supabase service client not configured.")
        raise HTTPException(status_code=500, detail="Supabase service client not configured.")

    return create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_ROLE_KEY)

def get_supabase_user_client(token: str) -> Client:
    """
    Devuelve un cliente de Supabase autenticado con el JWT del usuario.
    Este cliente aplicará las políticas de RLS de la base de datos.
    """
    if not config.SUPABASE_URL or not config.SUPABASE_ANON_KEY:
        logger.error("Supabase user client not configured.")
        raise HTTPException(status_code=500, detail="Supabase user client not configured.")

    client = create_client(config.SUPABASE_URL, config.SUPABASE_ANON_KEY)

    try:
        client.postgrest.auth(token)
    except Exception as exc:
        logger.exception("Error authenticating Supabase client with user token.")
        raise HTTPException(status_code=401, detail="Invalid authentication token.") from exc

    return client

# Cliente de servicio singleton para ser usado por otros módulos
service_supabase_client = get_supabase_service_client()
