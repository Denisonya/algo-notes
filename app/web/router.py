from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserLogin
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.note import NoteCreate, NoteUpdate

from app.services.auth_service import register_user_service, login_user_service
from app.services.category_service import (
    create_category_service,
    get_category_by_id_service,
    update_category_service,
    delete_category_service
)
from app.services.note_service import (
    create_note_service,
    get_note_by_id_service,
    update_note_service,
    delete_note_service
)

from app.repositories.category_repository import get_all_categories_by_user
from app.repositories.note_repository import get_all_notes_by_user
from app.repositories.user_repository import get_user_by_username

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.core.settings import settings

router = APIRouter(tags=["Web"])
templates = Jinja2Templates(directory="app/templates")


def get_username(request: Request):
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


def require_user(request: Request, db: Session):
    username = get_username(request)
    if not username:
        return None, RedirectResponse("/login", 303)

    user = get_user_by_username(db, username)
    if not user:
        return None, RedirectResponse("/login", 303)

    return user, None


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "username": get_username(request)}
    )


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "error": None, "username": None}
    )


@router.post("/register")
def register_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        register_user_service(UserCreate(username=username, password=password), db)
        return RedirectResponse("/login", 303)
    except AlreadyExistsError as e:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": str(e), "username": None}
        )


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": None, "username": None}
    )


@router.post("/login")
def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        token = login_user_service(UserLogin(username=username, password=password), db)

        response = RedirectResponse("/dashboard", 303)
        response.set_cookie(
            key="access_token",
            value=token["access_token"],
            httponly=True
        )
        return response

    except NotFoundError as e:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": str(e), "username": None}
        )


@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    user, redirect = require_user(request, db)
    if redirect:
        return redirect

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "username": user.username}
    )


# ===================== CATEGORIES =====================

@router.get("/categories")
def categories_page(request: Request, db: Session = Depends(get_db)):
    user, redirect = require_user(request, db)
    if redirect:
        return redirect

    return templates.TemplateResponse(
        "categories.html",
        {
            "request": request,
            "username": user.username,
            "categories": get_all_categories_by_user(db, user.id),
            "error": None
        }
    )


@router.post("/categories")
def create_category(
    request: Request,
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    user, redirect = require_user(request, db)
    if redirect:
        return redirect

    try:
        create_category_service(CategoryCreate(name=name), db, user)
        return RedirectResponse("/categories", 303)

    except AlreadyExistsError as e:
        return templates.TemplateResponse(
            "categories.html",
            {
                "request": request,
                "username": user.username,
                "categories": get_all_categories_by_user(db, user.id),
                "error": str(e)
            }
        )


@router.get("/categories/{category_id}/edit")
def edit_category_page(
    request: Request,
    category_id: int,
    db: Session = Depends(get_db)
):
    user, redirect = require_user(request, db)
    if redirect:
        return redirect

    category = get_category_by_id_service(category_id, db, user)

    return templates.TemplateResponse(
        "category_edit.html",
        {
            "request": request,
            "username": user.username,
            "category": category
        }
    )


@router.post("/categories/{category_id}/edit")
def edit_category_submit(
    request: Request,
    category_id: int,
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    user, redirect = require_user(request, db)
    if redirect:
        return redirect

    update_category_service(
        category_id,
        CategoryUpdate(name=name),
        db,
        user
    )
    return RedirectResponse("/categories", 303)


@router.post("/categories/{category_id}/delete")
def delete_category(
    request: Request,
    category_id: int,
    db: Session = Depends(get_db)
):
    user, redirect = require_user(request, db)
    if redirect:
        return redirect

    delete_category_service(category_id, db, user)
    return RedirectResponse("/categories", 303)


# ===================== NOTES =====================

@router.get("/notes")
def notes_page(request: Request, db: Session = Depends(get_db)):
    user, redirect = require_user(request, db)
    if redirect:
        return redirect

    return templates.TemplateResponse(
        "notes.html",
        {
            "request": request,
            "username": user.username,
            "notes": get_all_notes_by_user(db, user.id),
            "categories": get_all_categories_by_user(db, user.id),
            "error": None
        }
    )


@router.post("/notes")
def create_note(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    category_id: int = Form(...),
    db: Session = Depends(get_db)
):
    user, redirect = require_user(request, db)
    if redirect:
        return redirect

    create_note_service(
        NoteCreate(
            title=title,
            content=content,
            category_id=category_id
        ),
        db,
        user
    )
    return RedirectResponse("/notes", 303)


@router.get("/notes/{note_id}/edit")
def edit_note_page(
    request: Request,
    note_id: int,
    db: Session = Depends(get_db)
):
    user, redirect = require_user(request, db)
    if redirect:
        return redirect

    note = get_note_by_id_service(note_id, db, user)

    return templates.TemplateResponse(
        "note_edit.html",
        {
            "request": request,
            "username": user.username,
            "note": note,
            "categories": get_all_categories_by_user(db, user.id)
        }
    )


@router.post("/notes/{note_id}/edit")
def edit_note_submit(
    request: Request,
    note_id: int,
    title: str = Form(...),
    content: str = Form(...),
    category_id: int = Form(...),
    db: Session = Depends(get_db)
):
    user, redirect = require_user(request, db)
    if redirect:
        return redirect

    update_note_service(
        note_id,
        NoteUpdate(
            title=title,
            content=content,
            category_id=category_id
        ),
        db,
        user
    )
    return RedirectResponse("/notes", 303)


@router.post("/notes/{note_id}/delete")
def delete_note(
    request: Request,
    note_id: int,
    db: Session = Depends(get_db)
):
    user, redirect = require_user(request, db)
    if redirect:
        return redirect

    delete_note_service(note_id, db, user)
    return RedirectResponse("/notes", 303)


@router.get("/logout")
def logout():
    response = RedirectResponse("/", 303)
    response.delete_cookie("access_token")
    return response