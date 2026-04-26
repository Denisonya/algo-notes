from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserLogin, Token, UserRead
from app.services.auth_service import (
    register_user_service,
    login_user_service
)
from app.core.exceptions import AlreadyExistsError, NotFoundError

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
def register(
        data: UserCreate,
        db: Session = Depends(get_db)
):
    """
    Register a new user.

    Creates a user account and returns public user data
    (without password and without JWT token).

    :param data: UserCreate schema
    :param db: Database session
    :return: UserRead schema
    """
    try:
        return register_user_service(data, db)
    except AlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=Token
)
def login(
        data: UserLogin,
        db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token.

    :param data: UserLogin schema
    :param db: Database session
    :return: Token schema (access_token + token_type)
    """
    try:
        return login_user_service(data, db)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
