"""
Общие фикстуры для тестов:
- тестовая SQLite-база данных
- тестовая сессия базы данных
- тестовый пользователь
- тестовый FastAPI-клиент
- заголовки авторизации
"""

import os
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# В приложении объект settings создается сразу при импорте app.core.settings
# и если переменных окружения нет, Pydantic выдает ошибку еще до запуска тестов,
# поэтому здесь задаем переменные окружения для тестов по умолчанию
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("POSTGRES_DB", "test_db")
os.environ.setdefault("POSTGRES_USER", "test_user")
os.environ.setdefault("POSTGRES_PASSWORD", "test_password")

# Эти переменные окружения нужны для создания и проверки JWT-токенов в тестах
os.environ.setdefault("JWT_SECRET", "test-secret")
os.environ.setdefault("JWT_EXPIRE_MINUTES", "30")
os.environ.setdefault("JWT_ALGORITHM", "HS256")

# Импорты из приложения делаем после задания переменных окружения,
# потому что settings создается при импорте модулей app
from app.auth.security import create_access_token, hash_password
from app.dependencies.db import get_db
from app.models import Base, User
from app.routers import auth_router, category_router, note_router

# URL для подключения к тестовой базе данных
TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"

# StaticPool нужен, чтобы одна и та же SQLite-база в памяти сохранялась в рамках одного теста
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Создаем объект сессии для тестовой базы данных
TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Создает чистую тестовую базу данных для каждого теста.
    """
    Base.metadata.create_all(bind=engine)

    db_session = TestingSessionLocal()

    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def user(db: Session) -> User:
    """
    Создает тестового пользователя.

    Категории и заметки требуют user_id, поэтому для тестов нужен пользователь.
    """
    test_user = User(
        username="denis",
        hashed_password=hash_password("2006"),
    )

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    return test_user


@pytest.fixture()
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Создает тестовый FastAPI-клиент.

    Реальная зависимость get_db заменяется на тестовую сессию базы данных.
    """
    app = FastAPI()

    app.include_router(auth_router.router)
    app.include_router(category_router.router)
    app.include_router(note_router.router)

    def override_get_db() -> Generator[Session, None, None]:
        """
        Возвращает тестовую сессию базы данных внутри API-роутеров.
        """
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def auth_headers(user: User) -> dict[str, str]:
    """
    Создает заголовки авторизации для защищенных эндпоинтов.
    """
    token = create_access_token({"sub": user.username})

    return {
        "Authorization": f"Bearer {token}",
    }
