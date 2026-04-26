from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserLogin, Token
from app.services.auth_service import (
    register_user_service,
    login_user_service
)
from app.core.exceptions import AlreadyExistsError, NotFoundError

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """
    Register new user.
    """
    try:
        return register_user_service(data, db)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and return JWT token.
    """
    try:
        return login_user_service(data, db)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))