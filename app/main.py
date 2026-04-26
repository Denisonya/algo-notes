from fastapi import FastAPI

from app.core.database import engine
from app.models import Base
from app.routers import (
    note_router,
    category_router,
    auth_router
)

# Создание таблиц по метаданным моделей (только для разработки),
# если все необходимые таблицы уже имеются, то метод не создает таблицы заново
Base.metadata.create_all(bind=engine)  # bind принимает класс, который используется для подключения к БД

app = FastAPI(title="AlgoNotes-API", version="1.0.0")

# Подключение роутеров
app.include_router(note_router.router)
app.include_router(category_router.router)
app.include_router(auth_router.router)
