from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .database import engine, SessionLocal
from .models import Base, Note, Category

# создание базы данных и таблиц по метаданным моделей - только для разработки
# (если база данных и все необходимые таблицы уже имеются, то метод не создает заново таблицы)
Base.metadata.create_all(bind=engine)  # bind принимает класс, который используется для подключения к базе данных


# определяем зависимость через которую объект сессии базы данных будет передаваться в функции обработки
def get_db():
    db = SessionLocal()  # создаем объект сессии базы данных
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/")  # get, post, put, delete, patch
async def root():
    return {"message": "Hello from Algo-Notes"}


@app.post("/notes")
async def create_note(title: str, content: str, db: Session = Depends(get_db)):
    note = Note(title=title, content=content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@app.get("/notes")
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).all()
    return notes


@app.post("/categories")
def create_category(name: str, db: Session = Depends(get_db)):
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
