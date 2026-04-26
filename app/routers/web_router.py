from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import (
    register_user_service,
    login_user_service
)
from app.core.exceptions import (
    AlreadyExistsError,
    NotFoundError
)

router = APIRouter(tags=["Web"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# REGISTER

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "error": None}
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
        return RedirectResponse("/login", status_code=303)

    except AlreadyExistsError as e:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": str(e)}
        )


# LOGIN

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": None}
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
            {"request": request, "error": str(e)}
        )