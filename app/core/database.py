from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import settings

# Создание движка SQLAlchemy
engine = create_engine(settings.postgres_url)

# Создание класса сессии БД
SessionLocal = sessionmaker(
    autoflush=False,  # отключение автоматической синхронизации с БД
    autocommit=False,  # отключение автоматической фиксации изменений (транзакций) с БД
    bind=engine,  # привязка сессии БД к движку, который применяется для установки подключения
)
