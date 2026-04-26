from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Note


def get_all_notes(db: Session) -> list[Note]:
    """
    Retrieve all notes ordered by ID.

    :param db: Database session
    :return: List of Note objects
    """
    stmt = select(Note).order_by(Note.id)
    result = db.execute(stmt)
    return result.scalars().all()  # type: ignore


def get_all_notes_by_user(db: Session, user_id: int) -> list[Note]:
    """
    Retrieve all notes for a specific user.

    :param db: Database session
    :param user_id: User ID
    :return: List of Note objects
    """
    stmt = (
        select(Note)
        .where(Note.user_id == user_id)
        .order_by(Note.id)
    )
    result = db.execute(stmt)
    return result.scalars().all()  # type: ignore


def get_note_by_id(db: Session, note_id: int) -> Note | None:
    """
    Get note by its ID.

    :param db: Database session
    :param note_id: Note ID
    :return: Note object or None
    """
    stmt = select(Note).where(Note.id == note_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def get_notes_by_category_id(db: Session, category_id: int) -> list[Note]:
    """
    Retrieve all notes for a specific category.

    :param db: Database session
    :param category_id: Category ID
    :return: List of Note objects
    """
    stmt = select(Note).where(Note.category_id == category_id).order_by(Note.id)
    result = db.execute(stmt)
    return result.scalars().all()  # type: ignore


def create_note(db: Session, note: Note) -> Note:
    """
    Add a new note to the session and flush changes.

    :param db: Database session
    :param note: Note object
    :return: Note object (not committed)
    """
    db.add(note)
    db.flush()
    return note


def update_note(db: Session, note: Note) -> Note:
    """
    Flush updated note to the database.

    :param db: Database session
    :param note: Note object
    :return: Updated Note object
    """
    db.flush()
    return note


def delete_note(db: Session, note: Note) -> None:
    """
    Delete note from session.

    :param db: Database session
    :param note: Note object
    :return: None
    """
    db.delete(note)