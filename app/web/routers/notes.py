from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.dependencies.db import get_db
from app.repositories.category_repository import get_all_categories_by_user
from app.repositories.note_repository import get_all_notes_by_user
from app.schemas.note import NoteCreate, NoteUpdate
from app.services.note_service import (
    create_note_service,
    delete_note_service,
    get_note_by_id_service,
    update_note_service,
)
from app.web.dependencies import require_user_or_redirect
from app.web.templates import templates

router = APIRouter()


@router.get("/notes", response_class=HTMLResponse)
def notes_page(request: Request, db: Session = Depends(get_db)):
    """
    Render notes page for authenticated user.

    Shows notes and categories belonging to current user.

    :param request: FastAPI request object
    :param db: Database session
    :return: Rendered notes page or redirect response
    """
    user, redirect = require_user_or_redirect(request, db)

    if redirect:
        return redirect

    return templates.TemplateResponse(
        "notes.html",
        {
            "request": request,
            "username": user.username,
            "notes": get_all_notes_by_user(db, user.id),
            "categories": get_all_categories_by_user(db, user.id),
            "error": None,
        }
    )


@router.post("/notes", response_class=HTMLResponse)
def create_note(request: Request, title: str = Form(...), content: str = Form(...), category_id: int = Form(...),
                db: Session = Depends(get_db)):
    """
    Handle note creation form submit.

    Creates a new note for current authenticated user.
    Note can be created only inside user's own category.

    :param request: FastAPI request object
    :param title: Note title from form
    :param content: Note content from form
    :param category_id: Category ID from form
    :param db: Database session
    :return: Redirect response or rendered notes page
    """
    user, redirect = require_user_or_redirect(request, db)

    if redirect:
        return redirect

    try:
        create_note_service(
            NoteCreate(
                title=title,
                content=content,
                category_id=category_id
            ),
            db,
            user
        )

        return RedirectResponse("/notes", status_code=303)

    except NotFoundError as e:
        return templates.TemplateResponse(
            "notes.html",
            {
                "request": request,
                "username": user.username,
                "notes": get_all_notes_by_user(db, user.id),
                "categories": get_all_categories_by_user(db, user.id),
                "error": str(e),
            }
        )


@router.get("/notes/{note_id}/edit", response_class=HTMLResponse)
def edit_note_page(request: Request, note_id: int, db: Session = Depends(get_db)):
    """
    Render note edit page.

    Note can be opened only if it belongs to current user.

    :param request: FastAPI request object
    :param note_id: Note ID
    :param db: Database session
    :return: Rendered edit page or redirect response
    """
    user, redirect = require_user_or_redirect(request, db)

    if redirect:
        return redirect

    try:
        note = get_note_by_id_service(note_id, db, user)

    except NotFoundError:
        return RedirectResponse("/notes", status_code=303)

    return templates.TemplateResponse(
        "note_edit.html",
        {
            "request": request,
            "username": user.username,
            "note": note,
            "categories": get_all_categories_by_user(db, user.id),
        }
    )


@router.post("/notes/{note_id}/edit")
def edit_note_submit(request: Request, note_id: int, title: str = Form(...), content: str = Form(...),
                     category_id: int = Form(...), db: Session = Depends(get_db)):
    """
    Handle note edit form submit.

    Updates note only if it belongs to current user.
    New category must also belong to current user.

    :param request: FastAPI request object
    :param note_id: Note ID
    :param title: New note title from form
    :param content: New note content from form
    :param category_id: New category ID from form
    :param db: Database session
    :return: Redirect response
    """
    user, redirect = require_user_or_redirect(request, db)

    if redirect:
        return redirect

    try:
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

    except NotFoundError:
        return RedirectResponse("/notes", status_code=303)

    return RedirectResponse("/notes", status_code=303)


@router.post("/notes/{note_id}/delete")
def delete_note(request: Request, note_id: int, db: Session = Depends(get_db)):
    """
    Handle note delete form submit.

    Deletes note only if it belongs to current user.

    :param request: FastAPI request object
    :param note_id: Note ID
    :param db: Database session
    :return: Redirect response
    """
    user, redirect = require_user_or_redirect(request, db)

    if redirect:
        return redirect

    try:
        delete_note_service(note_id, db, user)

    except NotFoundError:
        return RedirectResponse("/notes", status_code=303)

    return RedirectResponse("/notes", status_code=303)
