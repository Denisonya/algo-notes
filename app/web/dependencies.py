from fastapi import Request
from jose import jwt, JWTError

from app.core.settings import settings


def get_current_username_from_cookie(request: Request) -> str | None:
    """
    Return username from JWT cookie.
    """
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
        return None