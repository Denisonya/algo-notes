import markdown

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from typing import Optional

from .database import engine, SessionLocal
from .models import Base, Note, Category
from .schemas import NoteCreate, NoteResponse, CategoryCreate, CategoryResponse

# создание базы данных и таблиц по метаданным моделей - только для разработки
# (если база данных и все необходимые таблицы уже имеются, то метод не создает заново таблицы)
Base.metadata.create_all(bind=engine)  # bind принимает класс, который используется для подключения к базе данных


# определяем зависимость через которую объект сессии базы данных будет передаваться в функции обработки
def get_db():
    """
    Get a database session
    :return: SQLAlchemy session object
    """
    db = SessionLocal()  # создаем объект сессии базы данных
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/")  # get, post, put, delete, patch
async def root():
    """
    Root endpoint
    :return: welcome message
    """
    return {"message": "Hello from Algo-Notes"}


@app.post("/notes", response_model=NoteResponse)
async def create_note(note_data: NoteCreate, db: Session = Depends(get_db)):
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


@app.get("/notes", response_model=list[NoteResponse])
async def get_notes(category_id: Optional[int] = None, db: Session = Depends(get_db)):
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


@app.post("/categories", response_model=CategoryResponse)
async def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new category
    :param category_data: Pydantic model with category fields (name)
    :param db: database session
    :return: created category
    """
    category = Category(**category_data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@app.get("/categories", response_model=list[CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    """
    Get all categories
    :return: list of categories
    """
    return db.query(Category).all()


@app.get("/notes/{note_id}/html", response_class=HTMLResponse)
def get_note_html(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).get(note_id)
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
