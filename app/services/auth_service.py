from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.repositories.user_repository import (
    get_user_by_username,
    create_user
)
from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.core.exceptions import AlreadyExistsError, NotFoundError


def register_user_service(data: UserCreate, db: Session) -> User:
    """
    Register a new user.

    :param data: UserCreate schema
    :param db: Database session
    :return: Created User object
    :raises AlreadyExistsError: If username already exists
    """
    if get_user_by_username(db, data.username):
        raise AlreadyExistsError("User already exists")

    user = User(
        username=data.username,
        hashed_password=hash_password(data.password)
    )

    try:
        create_user(db, user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise


def login_user_service(data: UserLogin, db: Session) -> dict:
    """
    Authenticate user and return JWT token.

    :param data: UserLogin schema
    :param db: Database session
    :return: Dictionary with access token and token type
    :raises NotFoundError: If credentials are invalid
    """
    user = get_user_by_username(db, data.username)

    if not user:
        raise NotFoundError("Invalid credentials")

    if not verify_password(data.password, user.hashed_password):
        raise NotFoundError("Invalid credentials")

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }