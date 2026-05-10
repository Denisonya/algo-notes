import pytest
from sqlalchemy.orm import Session

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import (
    login_user_service,
    register_user_service,
)


def test_register_user_service(db: Session):
    """
    Проверяет, что сервис регистрирует нового пользователя.
    """
    data = UserCreate(
        username="denis",
        password="2006",
    )

    user = register_user_service(data, db)

    assert user.id is not None
    assert user.username == "denis"
    assert user.hashed_password != "2006"


def test_register_duplicate_user(db: Session):
    """
    Проверяет, что нельзя зарегистрировать пользователя с повторяющимся username.
    """
    data = UserCreate(
        username="denis",
        password="2006",
    )

    register_user_service(data, db)

    with pytest.raises(AlreadyExistsError):
        register_user_service(data, db)


def test_login_user_service(db: Session):
    """
    Проверяет, что сервис возвращает токен при правильных данных.
    """
    register_user_service(
        UserCreate(
            username="denis",
            password="2006",
        ),
        db,
    )

    result = login_user_service(
        UserLogin(
            username="denis",
            password="2006",
        ),
        db,
    )

    assert "access_token" in result
    assert result["token_type"] == "bearer"


def test_login_wrong_password(db: Session):
    """
    Проверяет, что вход с неправильным паролем вызывает ошибку.
    """
    register_user_service(
        UserCreate(
            username="denis",
            password="2006",
        ),
        db,
    )

    with pytest.raises(NotFoundError):
        login_user_service(
            UserLogin(
                username="denis",
                password="wrong-password",
            ),
            db,
        )


def test_login_missing_user(db: Session):
    """
    Проверяет, что вход несуществующего пользователя вызывает ошибку.
    """
    with pytest.raises(NotFoundError):
        login_user_service(
            UserLogin(
                username="missing-user",
                password="missing-password",
            ),
            db,
        )