from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .database import engine, SessionLocal
from .models import Base, Note, Category

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


@app.post("/notes")
def create_note(title: str, content: str, category_id: int, db: Session = Depends(get_db)):
    """
    Create a new note
    :param title: title of the note
    :param content: content of the note
    :param category_id: id of category
    :param db: database session
    :return: created note
    """
    note = Note(title=title, content=content, category_id=category_id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@app.post("/categories")
def create_category(name: str, db: Session = Depends(get_db)):
    """
    Create a new category
    :param name: name of the category
    :param db: database session
    :return: created category
    """
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@app.get("/notes")
def get_notes(category_id: int = None, db: Session = Depends(get_db)):
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
