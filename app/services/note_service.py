from sqlalchemy.orm import Session

from ..models import Note, User
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

from ..repositories.category_repository import get_category_by_id


def get_all_notes_service(db: Session, user: User) -> list[Note]:
    """
    Retrieve all notes belonging to current user.

    :param db: Database session
    :param user: Current authenticated user
    :return: List of Note objects
    """
    return [n for n in get_all_notes(db) if n.user_id == user.id]


def get_notes_by_category_id_service(category_id: int, db: Session, user: User) -> list[Note]:
    """
    Retrieve notes by category ID.

    :param category_id: Category ID
    :param db: Database session
    :param user: Current authenticated user
    :return: List of Note objects
    """
    return [
        n for n in get_notes_by_category_id(db, category_id)
        if n.user_id == user.id
    ]


def get_note_by_id_service(note_id: int, db: Session, user: User) -> Note:
    """
    Retrieve note by ID.

    :param note_id: Note ID
    :param db: Database session
    :param user: Current authenticated user
    :return: Note object
    :raises NotFoundError: If note not found
    """
    note = get_note_by_id(db, note_id)

    if note is None or note.user_id != user.id:
        raise NotFoundError("Note not found")

    return note


def create_note_service(data: NoteCreate, db: Session, user: User) -> Note:
    """
    Create a new note with a given category.

    :param data: NoteCreate schema
    :param db: Database session
    :param user: Current authenticated user
    :return: Created Note object
    """
    category = get_category_by_id(db, data.category_id)

    if category is None or category.user_id != user.id:
        raise NotFoundError("Category not found")

    note = Note(
        **data.model_dump(),
        user_id=user.id
    )

    try:
        create_note(db, note)
        db.commit()
        db.refresh(note)
        return note
    except Exception:
        db.rollback()
        raise


def update_note_service(note_id: int, data: NoteUpdate, db: Session, user: User) -> Note:
    """
    Update note.

    :param note_id: Note ID
    :param data: NoteUpdate schema
    :param db: Database session
    :param user: Current authenticated user
    :return: Updated Note object
    """
    note = get_note_by_id(db, note_id)

    if note is None or note.user_id != user.id:
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


def patch_note_service(note_id: int, data: NotePatch, db: Session, user: User) -> Note:
    """
    Partially update note.

    :param note_id: Note ID
    :param data: NotePatch schema
    :param db: Database session
    :param user: Current authenticated user
    :return: Updated Note object
    """
    note = get_note_by_id(db, note_id)

    if note is None or note.user_id != user.id:
        raise NotFoundError("Note not found")

    try:
        apply_updates(note, data.model_dump(exclude_unset=True))

        update_note(db, note)
        db.commit()
        db.refresh(note)

        return note
    except Exception:
        db.rollback()
        raise


def delete_note_service(note_id: int, db: Session, user: User) -> None:
    """
    Delete note.

    :param note_id: Note ID
    :param db: Database session
    :param user: Current authenticated user
    :return: None
    """
    note = get_note_by_id(db, note_id)

    if note is None or note.user_id != user.id:
        raise NotFoundError("Note not found")

    try:
        delete_note(db, note)
        db.commit()
    except Exception:
        db.rollback()
        raise