from typing import Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models import Note, Category
from .. import schemas


def create_note(db: Session, note_data: schemas.NoteCreate):
    """
    Create a new note
    :param note_data: Pydantic model with note fields (title, content, category_id)
    :param db: database session
    :return: created note
    """
    # Проверка существования категории
    category = db.query(Category).get(note_data.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    note = Note(**note_data.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_notes(db: Session, category_id: Optional[int] = None):
    """
    Get all notes for a category if category_id is provided else all notes
    :param category_id: category id (optional)
    :param db: database session
    :return: list of notes
    """
    query = db.query(Note)
    if category_id:
        query = query.filter(Note.category_id == category_id)
    return query.all()


def get_note_by_id(db: Session, note_id: int):
    """
    Get note by id and return it as rendered HTML page
    :param note_id: note id
    :param db: database session
    :return: HTML representation of the note
    """
    note = db.query(Note).get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
