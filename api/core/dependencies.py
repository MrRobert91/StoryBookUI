from fastapi import Depends, HTTPException, Header
from api.services import user_service
from api.services.user_service import UserProfile

def get_authorization_token(authorization: str | None = Header(default=None)) -> str:
    """
    Extrae y devuelve el token 'Bearer' de la cabecera de autorización.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Falta la cabecera de autenticación 'Bearer' o su formato es inválido.",
        )
    return authorization.split(" ", 1)[1]

def get_authenticated_user(token: str = Depends(get_authorization_token)) -> UserProfile:
    """
    Dependencia de FastAPI que verifica el JWT y devuelve el perfil del usuario.
    Esta dependencia no comprueba los créditos.
    """
    return user_service.verify_jwt_and_get_user(token)

def get_user_with_credits(user: UserProfile = Depends(get_authenticated_user)) -> UserProfile:
    """
    Dependencia de FastAPI que se apoya en `get_authenticated_user`
    y además comprueba que el usuario tenga créditos disponibles.
    Si se usa esta dependencia, se puede asumir que el usuario está autenticado
    y tiene al menos 1 crédito.
    """
    user_service.check_user_credits(user)
    return user
