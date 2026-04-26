from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import (
    register_user_service,
    login_user_service
)
from app.repositories.category_repository import get_all_categories_by_user
from app.repositories.user_repository import get_user_by_username
from app.core.exceptions import (
    AlreadyExistsError,
    NotFoundError
)
from app.core.settings import settings

router = APIRouter(tags=["Web"])
templates = Jinja2Templates(directory="app/templates")


def get_current_username_from_cookie(request: Request) -> str | None:
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


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    username = get_current_username_from_cookie(request)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "username": username
        }
    )


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    username = get_current_username_from_cookie(request)

    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "error": None,
            "username": username
        }
    )


@router.post("/register", response_class=HTMLResponse)
def register_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        register_user_service(
            UserCreate(username=username, password=password),
            db
        )
        return RedirectResponse(url="/login", status_code=303)

    except AlreadyExistsError as e:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": str(e),
                "username": None
            }
        )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    username = get_current_username_from_cookie(request)

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": None,
            "username": username
        }
    )


@router.post("/login")
def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        token_data = login_user_service(
            UserLogin(username=username, password=password),
            db
        )

        response = RedirectResponse(
            url="/dashboard",
            status_code=303
        )

        response.set_cookie(
            key="access_token",
            value=token_data["access_token"],
            httponly=True
        )

        return response

    except NotFoundError as e:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": str(e),
                "username": None
            }
        )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    username = get_current_username_from_cookie(request)

    if not username:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "username": username
        }
    )


@router.get("/categories", response_class=HTMLResponse)
def categories_page(
    request: Request,
    db: Session = Depends(get_db)
):
    username = get_current_username_from_cookie(request)

    if not username:
        return RedirectResponse(url="/login", status_code=303)

    user = get_user_by_username(db, username)
    categories = get_all_categories_by_user(db, user.id)

    return templates.TemplateResponse(
        "categories.html",
        {
            "request": request,
            "username": username,
            "categories": categories
        }
    )


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response