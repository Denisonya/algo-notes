import markdown

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import note
from ..services import note_service

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", response_model=note.NoteResponse)
def create_note(data: note.NoteCreate, db: Session = Depends(get_db)):
    """
    Create a new note.

    :param data: Pydantic model with note fields (title, content, category_id)
    :param db: Database session
    :return: Created note
    """
    return note_service.create_note(db, data)


@router.get("/", response_model=list[note.NoteResponse])
def get_all_notes(db: Session = Depends(get_db)):
    """
    Retrieve all notes.

    :param db: Database session
    :return: List of all notes
    """
    return note_service.get_all_notes(db)


@router.get("/category/{category_id}", response_model=list[note.NoteResponse])
def get_notes_by_category(category_id: int, db: Session = Depends(get_db)):
    """
    Get all notes for a specific category.

    :param category_id: Category ID
    :param db: Database session
    :return: List of notes
    """
    return note_service.get_notes_by_category_id(db, category_id)


@router.get("/{note_id}", response_model=note.NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """
    Get note by ID.

    :param note_id: Note ID
    :param db: Database session
    :return: Note object
    """
    return note_service.get_note_by_id(db, note_id)


@router.get("/{note_id}/html", response_class=HTMLResponse)
def get_note_html(note_id: int, db: Session = Depends(get_db)):
    """
    Get note by ID and return it as rendered HTML page.

    :param note_id: Note ID
    :param db: Database session
    :return: HTML representation of the note
    """
    note_obj = note_service.get_note_by_id(db, note_id)

    html_content = markdown.markdown(note_obj.content)

    return f"""
    <html>
        <head>
            <title>{note_obj.title}</title>
        </head>
        <body>
            <h1>{note_obj.title}</h1>
            {html_content}
        </body>
    </html>
    """