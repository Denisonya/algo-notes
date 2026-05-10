from fastapi import Request
from fastapi.responses import RedirectResponse
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.models.user import User
from app.repositories.user_repository import get_user_by_username


def get_current_username_from_cookie(request: Request) -> str | None:
    """
    Return username from JWT cookie.

    Reads JWT token from the access_token cookie, decodes it, and extracts username from the "sub" field.

    :param request: FastAPI request object
    :return: Username from token or None if token is missing/invalid
    """
    # Web-часть хранит JWT не в Authorization header, а в cookie
    token = request.cookies.get("access_token")

    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )

        return payload.get("sub")

    except JWTError:
        # Если токен поврежден, просрочен или подписан неверно, считаем пользователя неавторизованным
        return None


def get_current_user_from_cookie(request: Request, db: Session) -> User | None:
    """
    Return current authenticated user from JWT cookie.

    First extracts username from cookie token, then loads user from the database.

    :param request: FastAPI request object
    :param db: Database session
    :return: User model instance or None
    """
    username = get_current_username_from_cookie(request)

    if not username:
        return None

    return get_user_by_username(db, username)


def require_user_or_redirect(request: Request, db: Session) -> tuple[User | None, RedirectResponse | None]:
    """
    Require authenticated user for protected web pages.

    If user is authenticated, returns user and None.
    If user is not authenticated, returns None and redirect response.

    :param request: FastAPI request object
    :param db: Database session
    :return: Tuple of user and optional redirect response
    """
    user = get_current_user_from_cookie(request, db)

    if user is None:
        return None, RedirectResponse("/login", status_code=303)

    return user, None
