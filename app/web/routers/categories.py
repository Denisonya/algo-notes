from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.dependencies.db import get_db
from app.repositories.category_repository import get_all_categories_by_user
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.category_service import (
    create_category_service,
    delete_category_service,
    get_category_by_id_service,
    update_category_service,
)
from app.web.dependencies import require_user_or_redirect
from app.web.templates import templates

router = APIRouter()


@router.get("/categories", response_class=HTMLResponse)
def categories_page(request: Request, db: Session = Depends(get_db)):
    """
    Render categories page for authenticated user.

    Shows all categories belonging to current user.

    :param request: FastAPI request object
    :param db: Database session
    :return: Rendered categories page or redirect response
    """
    user, redirect = require_user_or_redirect(request, db)

    if redirect:
        return redirect

    return templates.TemplateResponse(
        "categories.html",
        {
            "request": request,
            "username": user.username,
            "categories": get_all_categories_by_user(db, user.id),
            "error": None,
        }
    )


@router.post("/categories", response_class=HTMLResponse)
def create_category(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    """
    Handle category creation form submit.

    Creates a new category for current authenticated user.
    If category already exists, renders categories page with error.

    :param request: FastAPI request object
    :param name: Category name from form
    :param db: Database session
    :return: Redirect response or rendered categories page
    """
    user, redirect = require_user_or_redirect(request, db)

    if redirect:
        return redirect

    try:
        create_category_service(
            CategoryCreate(name=name),
            db,
            user
        )

        return RedirectResponse("/categories", status_code=303)

    except AlreadyExistsError as e:
        return templates.TemplateResponse(
            "categories.html",
            {
                "request": request,
                "username": user.username,
                "categories": get_all_categories_by_user(db, user.id),
                "error": str(e),
            }
        )


@router.get("/categories/{category_id}/edit", response_class=HTMLResponse)
def edit_category_page(request: Request, category_id: int, db: Session = Depends(get_db)):
    """
    Render category edit page.

    Category can be opened only if it belongs to current user.

    :param request: FastAPI request object
    :param category_id: Category ID
    :param db: Database session
    :return: Rendered edit page or redirect response
    """
    user, redirect = require_user_or_redirect(request, db)

    if redirect:
        return redirect

    try:
        category = get_category_by_id_service(category_id, db, user)

    except NotFoundError:
        return RedirectResponse("/categories", status_code=303)

    return templates.TemplateResponse(
        "category_edit.html",
        {
            "request": request,
            "username": user.username,
            "category": category,
        }
    )


@router.post("/categories/{category_id}/edit")
def edit_category_submit(request: Request, category_id: int, name: str = Form(...), db: Session = Depends(get_db)):
    """
    Handle category edit form submit.

    Updates category name only if category belongs to current user.

    :param request: FastAPI request object
    :param category_id: Category ID
    :param name: New category name from form
    :param db: Database session
    :return: Redirect response
    """
    user, redirect = require_user_or_redirect(request, db)

    if redirect:
        return redirect

    try:
        update_category_service(
            category_id,
            CategoryUpdate(name=name),
            db,
            user
        )

    except NotFoundError:
        return RedirectResponse("/categories", status_code=303)

    return RedirectResponse("/categories", status_code=303)


@router.post("/categories/{category_id}/delete")
def delete_category(request: Request, category_id: int, db: Session = Depends(get_db)):
    """
    Handle category delete form submit.

    Deletes category only if it belongs to current user.
    Related notes are deleted by SQLAlchemy cascade.

    :param request: FastAPI request object
    :param category_id: Category ID
    :param db: Database session
    :return: Redirect response
    """
    user, redirect = require_user_or_redirect(request, db)

    if redirect:
        return redirect

    try:
        delete_category_service(category_id, db, user)

    except NotFoundError:
        return RedirectResponse("/categories", status_code=303)

    return RedirectResponse("/categories", status_code=303)
