from fastapi import FastAPI

from app.core.database import engine
from app.models import Base
from app.routers import notes, categories

app = FastAPI()

# Создание таблиц по метаданным моделей (только для разработки),
# если все необходимые таблицы уже имеются, то метод не создает таблицы заново
Base.metadata.create_all(bind=engine)  # bind принимает класс, который используется для подключения к БД

# Подключение роутеров
app.include_router(notes.router)
app.include_router(categories.router)
