from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.note import NoteCreate, NoteRead, NoteUpdate, NotePatch
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
def get_all_notes(db: Session = Depends(get_db)):
    try:
        return get_all_notes_service(db)
    except SQLAlchemyError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "DB error")


@router.get("/category/{category_id}", response_model=list[NoteRead])
def get_notes_by_category_id(category_id: int, db: Session = Depends(get_db)):
    try:
        return get_notes_by_category_id_service(category_id, db)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.get("/{note_id}", response_model=NoteRead)
def get_note_by_id(note_id: int, db: Session = Depends(get_db)):
    try:
        return get_note_by_id_service(note_id, db)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(data: NoteCreate, db: Session = Depends(get_db)):
    try:
        return create_note_service(data, db)
    except SQLAlchemyError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "DB error")


@router.put("/{note_id}", response_model=NoteRead)
def update_note(note_id: int, data: NoteUpdate, db: Session = Depends(get_db)):
    try:
        return update_note_service(note_id, data, db)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.patch("/{note_id}", response_model=NoteRead)
def patch_note(note_id: int, data: NotePatch, db: Session = Depends(get_db)):
    try:
        return patch_note_service(note_id, data, db)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    try:
        delete_note_service(note_id, db)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
    except SQLAlchemyError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "DB error")
