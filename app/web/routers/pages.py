from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.web.dependencies import (
    get_current_username_from_cookie,
    require_user_or_redirect,
)
from app.web.templates import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    Render home page.

    Shows different navigation links depending on whether user is authenticated or not.

    :param request: FastAPI request object
    :return: Rendered index page
    """
    # На главной странице авторизация не обязательна, но имя пользователя нужно для корректного отображения меню
    username = get_current_username_from_cookie(request)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "username": username,
        }
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    """
    Render dashboard page for authenticated user.

    If user is not authenticated, redirects to login page.

    :param request: FastAPI request object
    :param db: Database session
    :return: Rendered dashboard page or redirect response
    """
    user, redirect = require_user_or_redirect(request, db)

    if redirect:
        return redirect

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "username": user.username,
        }
    )
