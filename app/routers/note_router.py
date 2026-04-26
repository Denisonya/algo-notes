from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

from app.schemas.note import (
    NoteCreate,
    NoteRead,
    NoteUpdate,
    NotePatch
)

from app.services.note_service import (
    get_all_notes_service,
    get_notes_by_category_id_service,
    get_note_by_id_service,
    create_note_service,
    update_note_service,
    patch_note_service,
    delete_note_service,
)

from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/", response_model=list[NoteRead])
def get_all_notes(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Get all notes for current authenticated user.
    """
    try:
        return get_all_notes_service(db, user)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )


@router.get("/category/{category_id}", response_model=list[NoteRead])
def get_notes_by_category_id(
    category_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Get all notes for a specific category (only user-owned).
    """
    try:
        return get_notes_by_category_id_service(category_id, db, user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{note_id}", response_model=NoteRead)
def get_note_by_id(
    note_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Get note by ID (only if belongs to current user).
    """
    try:
        return get_note_by_id_service(note_id, db, user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(
    data: NoteCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Create new note for current user.
    """
    try:
        return create_note_service(data, db, user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{note_id}", response_model=NoteRead)
def update_note(
    note_id: int,
    data: NoteUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Update note (only if belongs to current user).
    """
    try:
        return update_note_service(note_id, data, db, user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{note_id}", response_model=NoteRead)
def patch_note(
    note_id: int,
    data: NotePatch,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Partially update note (only if belongs to current user).
    """
    try:
        return patch_note_service(note_id, data, db, user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Delete note (only if belongs to current user).
    """
    try:
        delete_note_service(note_id, db, user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )