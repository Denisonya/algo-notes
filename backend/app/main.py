from fastapi import Depends, FastAPI

from .database import engine, SessionLocal
from .models import Base

# создание базы данных и таблиц по метаданным моделей
# (если база данных и все необходимые таблицы уже имеются, то метод не создает заново таблицы)
Base.metadata.create_all(bind=engine)  # bind принимает класс, который используется для подключения к базе данных

app = FastAPI()


# определяем зависимость через которую объект сессии базы данных будет передаваться в функции обработки
def get_db():
    db = SessionLocal()  # создаем объект сессии базы данных.
    try:
        yield db
    finally:
        db.close()


@app.get("/")  # get, post, put, delete, patch
async def root():
    return {"message": "Hello from Algo-Notes"}
