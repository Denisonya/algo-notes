from sqlalchemy.orm import Session
from ..models.note import Note


def create(db: Session, data: dict) -> Note:
    """
    Create a new note.

    :param db: Database session
    :param data: Dictionary with note fields
    :return: Created Note object
    """
    note = Note(**data)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_by_category_id(db: Session, category_id: int) -> list[Note]:
    """
    Get notes by category ID.

    :param db: Database session
    :param category_id: Category ID
    :return: List of notes
    """
    return db.query(Note).filter(Note.category_id == category_id).all()


def get_by_id(db: Session, note_id: int) -> Note | None:
    """
    Get note by its ID.

    :param db: Database session
    :param note_id: Note ID
    :return: Note object or None
    """
    return db.query(Note).get(note_id)


def get_all(db: Session) -> list[Note]:
    """
    Retrieve all notes.

    :param db: Database session
    :return: List of notes
    """
    return db.query(Note).all()
