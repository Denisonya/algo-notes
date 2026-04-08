import markdown

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas
from ..services import note_service

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", response_model=schemas.NoteResponse)
def create_note(note_data: schemas.NoteCreate, db: Session = Depends(get_db)):
    """
    Create a new note
    :param note_data: Pydantic model with note fields (title, content, category_id)
    :param db: database session
    :return: created note
    """
    return note_service.create_note(db, note_data)


@router.get("/", response_model=list[schemas.NoteResponse])
def get_notes(category_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Get all notes for a category if category_id is provided else all notes
    :param category_id: category id (optional)
    :param db: database session
    :return: list of notes
    """
    return note_service.get_notes(db, category_id)


@router.get("/{note_id}/html", response_class=HTMLResponse)
def get_note_html(note_id: int, db: Session = Depends(get_db)):
    """
    Get note by id and return it as rendered HTML page
    :param note_id: note id
    :param db: database session
    :return: HTML representation of the note
    """
    note = note_service.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    html_content = markdown.markdown(note.content)
    return f"""
    <html>
        <head>
            <title>{note.title}</title>
        </head>
        <body>
            <h1>{note.title}</h1>
            {html_content}
        </body>
    </html>
    """
