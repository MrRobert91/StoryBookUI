from fastapi import HTTPException
from supabase import Client
import logging
import jwt
from datetime import datetime, timezone

from api.services.supabase_client import get_supabase_user_client, service_supabase_client

logger = logging.getLogger(__name__)

class UserProfile:
    """Modelo para almacenar los datos relevantes del perfil del usuario."""
    def __init__(self, user_id: str, credits: int, plan: str, supabase_client: Client, token: str):
        self.id = user_id
        self.credits = credits
        self.plan = plan
        self.client = supabase_client
        self.token = token

def _log_token_details(token: str):
    """Función auxiliar para decodificar y registrar detalles de un JWT sin validarlo."""
    try:
        # Decodificar el token sin verificar la firma para inspeccionar los claims
        decoded_token = jwt.decode(token, options={"verify_signature": False})

        user_id = decoded_token.get("sub")
        exp_timestamp = decoded_token.get("exp")

        exp_datetime = "N/A"
        is_expired = "N/A"

        if exp_timestamp:
            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc).isoformat()
            is_expired = datetime.now(timezone.utc).timestamp() > exp_timestamp

        logger.warning(
            "Token details: sub=%s, exp=%s, is_expired=%s",
            user_id, exp_datetime, is_expired
        )
    except jwt.DecodeError:
        logger.warning("Could not decode the provided JWT.")
    except Exception:
        logger.exception("An unexpected error occurred while decoding the token.")


def verify_jwt_and_get_user(token: str) -> UserProfile:
    """
    Verifica el JWT de un usuario, obtiene su perfil y devuelve un objeto UserProfile.
    Eleva una HTTPException si el token es inválido o el usuario no existe.
    """
    logger.info("Verifying JWT and fetching user profile.")

    # 1. Obtener un cliente de Supabase autenticado con el token del usuario.
    supabase = get_supabase_user_client(token)

    # 2. Verificar el token obteniendo los datos del usuario.
    try:
        # CORRECCIÓN: Pasar el token explícitamente a la función get_user.
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            logger.warning("Supabase did not return a user for the token.")
            _log_token_details(token)
            raise HTTPException(status_code=401, detail="Invalid or expired token.")
        user_id = user_response.user.id
        logger.info("JWT is valid for user_id: %s", user_id)
    except Exception as exc:
        logger.exception("Error verifying JWT with Supabase.")
        _log_token_details(token)
        raise HTTPException(status_code=401, detail="Invalid or expired token.") from exc

    # 3. Obtener el perfil del usuario para verificar créditos y plan.
    try:
        profile_response = (
            supabase.table("profiles")
            .select("credits", "plan")
            .eq("id", user_id)
            .single()
            .execute()
        )

        profile_data = profile_response.data or {}
        logger.info("User profile data: %s", profile_data)

        if not profile_data:
             logger.warning("No profile found for user_id: %s", user_id)
             raise HTTPException(status_code=404, detail="User profile not found.")

        # CORRECCIÓN: Pasar el token al crear el objeto UserProfile.
        return UserProfile(
            user_id=user_id,
            credits=profile_data.get("credits", 0),
            plan=profile_data.get("plan", "free"),
            supabase_client=supabase,
            token=token
        )
    except Exception as exc:
        logger.exception("Failed to fetch user profile from database.")
        raise HTTPException(status_code=500, detail="Could not retrieve user profile.") from exc

def check_user_credits(user: UserProfile):
    """
    Verifica si un usuario tiene créditos suficientes.
    Eleva una HTTPException si el usuario no tiene créditos.
    """
    if user.credits <= 0:
        logger.warning("User %s has no available credits.", user.id)
        raise HTTPException(
            status_code=402,
            detail="No tienes créditos disponibles. Suscríbete para continuar.",
        )
    logger.info("User %s has %d credits.", user.id, user.credits)

def deduct_credit(user: UserProfile):
    """
    Resta un crédito del perfil de un usuario.
    """
    try:
        new_credits = user.credits - 1
        (
            user.client.table("profiles")
            .update({"credits": new_credits})
            .eq("id", user.id)
            .execute()
        )
        logger.info("Credit deducted for user %s. New balance: %d", user.id, new_credits)
    except Exception:
        logger.exception("Failed to deduct credit for user %s.", user.id)
        # No elevamos una excepción aquí para no interrumpir el flujo principal
        # si solo falla la deducción de crédito, pero sí lo registramos.
