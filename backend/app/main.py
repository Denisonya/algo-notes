from fastapi import FastAPI

from .database import engine
from .models import Base
from .routers import notes, categories

# Создание таблиц по метаданным моделей (только для разработки), если все необходимые таблицы уже имеются, то метод не создает таблицы заново
Base.metadata.create_all(bind=engine)  # bind принимает класс, который используется для подключения к БД

app = FastAPI()

# Подключение роутеров
app.include_router(notes.router)
app.include_router(categories.router)
