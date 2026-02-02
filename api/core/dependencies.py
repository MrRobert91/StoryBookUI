from fastapi import Depends, HTTPException, Header, Query, status
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

def get_token_from_query(token: str | None = Query(default=None)) -> str:
    """
    Extrae el token del parámetro de consulta 'token' para WebSockets.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
        )
    return token

def get_authenticated_user(token: str = Depends(get_authorization_token)) -> UserProfile:
    """
    Dependencia de FastAPI que verifica el JWT y devuelve el perfil del usuario.
    Esta dependencia no comprueba los créditos.
    """
    return user_service.verify_jwt_and_get_user(token)

def get_authenticated_socket_user(token: str = Depends(get_token_from_query)) -> UserProfile:
    """
    Dependencia compatible con WebSocket que verifica el JWT y devuelve el perfil del usuario.
    Reutiliza la lógica de 'user_service.verify_jwt_and_get_user', pero captura excepciones para WS.
    """
    try:
        return user_service.verify_jwt_and_get_user(token)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

def get_user_with_credits(user: UserProfile = Depends(get_authenticated_user)) -> UserProfile:
    """
    Dependencia de FastAPI que se apoya en `get_authenticated_user`
    y además comprueba que el usuario tenga créditos disponibles.
    Si se usa esta dependencia, se puede asumir que el usuario está autenticado
    y tiene al menos 1 crédito.
    """
    user_service.check_user_credits(user)
    return user
