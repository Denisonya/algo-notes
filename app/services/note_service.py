from sqlalchemy.orm import Session

from ..models import Note
from ..schemas.note import NoteCreate, NoteUpdate, NotePatch
from ..core.exceptions import NotFoundError
from ..utils.common import apply_updates

from ..repositories.note_repository import (
    get_all_notes,
    get_note_by_id,
    get_notes_by_category_id,
    create_note,
    update_note,
    delete_note,
)


def get_all_notes_service(db: Session) -> list[Note]:
    """
    Retrieve all notes.

    :param db: Database session
    :return: List of Note objects
    """
    return get_all_notes(db)


def get_notes_by_category_id_service(category_id: int, db: Session) -> list[Note]:
    """
    Retrieve notes by category ID.

    :param category_id: Category ID
    :param db: Database session
    :return: List of Note objects
    """
    return get_notes_by_category_id(db, category_id)


def get_note_by_id_service(note_id: int, db: Session) -> Note:
    """
    Retrieve note by ID.

    :param note_id: Note ID
    :param db: Database session
    :return: Note object
    :raises NotFoundError: If note not found
    """
    note = get_note_by_id(db, note_id)

    if note is None:
        raise NotFoundError("Note not found")

    return note


def create_note_service(data: NoteCreate, db: Session) -> Note:
    """
    Create a new note.

    :param data: NoteCreate schema
    :param db: Database session
    :return: Created Note object
    """
    note = Note(**data.model_dump())

    try:
        create_note(db, note)
        db.commit()
        db.refresh(note)
        return note
    except Exception:
        db.rollback()
        raise


def update_note_service(note_id: int, data: NoteUpdate, db: Session) -> Note:
    """
    Update note.

    :param note_id: Note ID
    :param data: NoteUpdate schema
    :param db: Database session
    :return: Updated Note object
    :raises NotFoundError: If note not found
    """
    note = get_note_by_id(db, note_id)

    if note is None:
        raise NotFoundError("Note not found")

    try:
        note.title = data.title
        note.content = data.content
        note.category_id = data.category_id

        update_note(db, note)
        db.commit()
        db.refresh(note)

        return note
    except Exception:
        db.rollback()
        raise


def patch_note_service(note_id: int, data: NotePatch, db: Session) -> Note:
    """
    Partial update note.

    :param note_id: Note ID
    :param data: NotePatch schema
    :param db: Database session
    :return: Partial updated Note object
    :raises NotFoundError: If note not found
    """
    note = get_note_by_id(db, note_id)

    if note is None:
        raise NotFoundError("Note not found")

    try:
        apply_updates(note, data.model_dump(
            exclude_unset=True))  # exclude_unset - передаем словарь только с измененными полями (поля, которые не были переданы, остаются прежними)

        update_note(db, note)
        db.commit()
        db.refresh(note)

        return note
    except Exception:
        db.rollback()
        raise


def delete_note_service(note_id: int, db: Session) -> Note:
    """
    Delete note.

    :param note_id: Note ID
    :param db: Database session
    :return: Deleted Note object
    :raises NotFoundError: If note not found
    """
    note = get_note_by_id(db, note_id)

    if note is None:
        raise NotFoundError("Note not found")

    try:
        delete_note(db, note)
        db.commit()
        return note
    except Exception:
        db.rollback()
        raise
