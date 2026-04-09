from typing import Generator

from sqlalchemy.orm import Session
from ..core.database import SessionLocal


# Определяем зависимость, через которую объект сессии БД будет передаваться в функции обработки
def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session.

    :yield: SQLAlchemy Session object
    """
    # Создаем объект сессии БД
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
