from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..dependencies.db import get_db
from ..schemas import note
from ..services import note_service

from ..utils.markdown import render_markdown

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", response_model=note.NoteResponse)
def create_note(data: note.NoteCreate, db: Session = Depends(get_db)) -> note.NoteResponse:
    """
    Create a new note.

    :param data: Note input data
    :param db: Database session
    :return: Created note
    """
    return note_service.create_note(db, data)


@router.get("/", response_model=list[note.NoteResponse])
def get_all_notes(db: Session = Depends(get_db)) -> list[note.NoteResponse]:
    """
    Retrieve all notes.

    :param db: Database session
    :return: List of notes
    """
    return note_service.get_all_notes(db)


@router.get("/category/{category_id}", response_model=list[note.NoteResponse])
def get_notes_by_category(category_id: int, db: Session = Depends(get_db)) -> list[note.NoteResponse]:
    """
    Retrieve notes by category.

    :param category_id: Category ID
    :param db: Database session
    :return: List of notes
    """
    return note_service.get_notes_by_category_id(db, category_id)


@router.get("/{note_id}", response_model=note.NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)) -> note.NoteResponse:
    """
    Get note by ID.

    :param note_id: Note ID
    :param db: Database session
    :return: Note object
    """
    return note_service.get_note_by_id(db, note_id)


@router.get("/{note_id}/html", response_class=HTMLResponse)
def get_note_html(note_id: int, db: Session = Depends(get_db)) -> HTMLResponse:
    """
    Get note as HTML.

    :param note_id: Note ID
    :param db: Database session
    :return: HTML page with rendered Markdown
    """
    note_obj = note_service.get_note_by_id(db, note_id)

    html_content = render_markdown(note_obj.content)

    return HTMLResponse(status_code=200, content=html_content)
