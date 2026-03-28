from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# определение строки подключения
DATABASE_URL = "postgresql://algo_user:algo_password@db:5432/algo_notes"  # db - это имя сервиса из docker-compose (не localhost)

# создание движка SqlAlchemy
engine = create_engine(DATABASE_URL)

# создание класса сессии базы данных
SessionLocal = sessionmaker(autoflush=False, autocommit=False,
                            bind=engine)  # параметр bind привязывает сессию БД к определенному движку, который применяется для установки подключения

# создаем базовый класс для моделей
Base = declarative_base()
