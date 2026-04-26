from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from ..core.settings import settings
from app.dependencies.db import get_db
from app.repositories.user_repository import get_user_by_username
from app.models.user import User

# Схема авторизации Bearer Token
# Ожидает заголовок: Authorization: Bearer <token>
security = HTTPBearer()


def get_current_username(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
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

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        # Возвращаем username
        return username

    except JWTError:
        # Ошибка токена: неверная подпись, истек срок и прочее
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def get_current_user(
    username: str = Depends(get_current_username),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from database.

    Converts username from JWT into full User object.

    :param username: Username extracted from token
    :param db: Database session
    :return: User model instance
    """
    user = get_user_by_username(db, username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user