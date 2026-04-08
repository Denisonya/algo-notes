from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..repositories import note_repository, category_repository
from ..schemas import note as note_schema
from ..models.note import Note


def create_note(db: Session, data: note_schema.NoteCreate) -> Note:
    """
    Create a new note.

    :param db: Database session
    :param data: Note input data
    :return: Created Note object
    :raises HTTPException: If category not found
    """
    category = category_repository.get_by_id(db, data.category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return note_repository.create(db, data.model_dump())


def get_notes_by_category_id(db: Session, category_id: int) -> list[Note]:
    """
    Retrieve notes by category ID.

    :param db: Database session
    :param category_id: Category ID
    :return: List of notes
    :raises HTTPException: If category not found
    """
    # Проверка существования категории
    category = category_repository.get_by_id(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return note_repository.get_by_category_id(db, category_id)


def get_all_notes(db: Session) -> list[Note]:
    """
    Retrieve all notes.

    :param db: Database session
    :return: List of notes
    """
    return note_repository.get_all(db)


def get_note_by_id(db: Session, note_id: int) -> Note:
    """
    Get note by its ID.

    :param db: Database session
    :param note_id: Note ID
    :return: Note object
    :raises HTTPException: If note not found
    """
    note = note_repository.get_by_id(db, note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note
