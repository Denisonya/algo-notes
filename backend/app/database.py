from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()

# Получаем строку подключения из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL не найдена в переменных окружения")

# Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL)

# Создание класса сессии БД
SessionLocal = sessionmaker(
    autoflush=False,  # отключение автоматической синхронизации с БД
    autocommit=False,  # отключение автоматической фиксации изменений (транзакций) с БД
    bind=engine,
    # параметр bind привязывает сессию БД к определенному движку, который применяется для установки подключения
)

# Создаем базовый класс для моделей
Base = declarative_base()


# Определяем зависимость, через которую объект сессии БД будет передаваться в функции обработки
def get_db():
    """
    Get a database session
    :return: SQLAlchemy session object
    """
    # Создаем объект сессии БД
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
