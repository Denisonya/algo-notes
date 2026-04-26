from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from ..core.settings import settings

# Схема авторизации Bearer Token
# Ожидает заголовок: Authorization: Bearer <token>
security = HTTPBearer()


def get_current_username(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Get current username from JWT token.

    Extracts token from Authorization header,
    decodes it and returns username from payload.

    :param credentials: Bearer token credentials
    :return: Username from token
    :raises HTTPException: If token is invalid
    """
    # Получаем сам токен без слова Bearer
    token = credentials.credentials

    try:
        # Декодируем JWT токен
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )

        # Возвращаем username
        return payload["sub"]

    except JWTError:
        # Ошибка токена: неверная подпись, истек срок и прочее
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
