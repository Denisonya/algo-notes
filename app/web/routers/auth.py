from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import (
    login_user_service,
    register_user_service,
)
from app.web.templates import templates

router = APIRouter()


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    """
    Render registration page.

    :param request: FastAPI request object
    :return: Rendered registration page
    """
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "error": None,
            "username": None,
        }
    )


@router.post("/register", response_class=HTMLResponse)
def register_submit(request: Request, username: str = Form(...), password: str = Form(...),
                    db: Session = Depends(get_db)):
    """
    Handle registration form submit.

    Creates a new user account. If username already exists, renders the same page with an error message.

    :param request: FastAPI request object
    :param username: Username from form
    :param password: Password from form
    :param db: Database session
    :return: Redirect response or rendered registration page
    """
    try:
        register_user_service(
            UserCreate(username=username, password=password),
            db
        )

        return RedirectResponse("/login", status_code=303)

    except AlreadyExistsError as e:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": str(e),
                "username": None,
            }
        )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    """
    Render login page.

    :param request: FastAPI request object
    :return: Rendered login page
    """
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": None,
            "username": None,
        }
    )


@router.post("/login", response_class=HTMLResponse)
def login_submit(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """
    Handle login form submit.

    Authenticates user, creates JWT token and stores it in an HTTP-only cookie.

    :param request: FastAPI request object
    :param username: Username from form
    :param password: Password from form
    :param db: Database session
    :return: Redirect response or rendered login page
    """
    try:
        token = login_user_service(
            UserLogin(username=username, password=password),
            db
        )

        response = RedirectResponse("/dashboard", status_code=303)

        response.set_cookie(
            key="access_token",
            value=token["access_token"],
            httponly=True,
            samesite="lax"
        )

        return response

    except NotFoundError as e:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": str(e),
                "username": None,
            }
        )


@router.get("/logout")
def logout():
    """
    Log out current user.

    Deletes JWT cookie and redirects user to home page.

    :return: Redirect response
    """
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")

    return response
