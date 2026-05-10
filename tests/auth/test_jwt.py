import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

from app.auth.dependencies import get_current_username
from app.auth.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.core.settings import settings


def test_hash_password():
    """
    Проверяет, что хеш пароля не равен исходному паролю.
    """
    password = "2006"

    hashed = hash_password(password)

    assert hashed != password


def test_verify_password_success():
    """
    Проверяет, что правильный пароль проходит проверку.
    """
    password = "2006"

    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_failure():
    """
    Проверяет, что неправильный пароль не проходит проверку.
    """
    password = "2006"

    hashed = hash_password(password)

    assert verify_password("wrong-password", hashed) is False


def test_create_access_token():
    """
    Проверяет, что access token содержит username в поле sub.
    """
    token = create_access_token({"sub": "denis"})

    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )

    assert payload["sub"] == "denis"


def test_get_current_username_from_valid_token():
    """
    Проверяет, что username можно получить из правильного JWT.
    """
    token = create_access_token({"sub": "denis"})

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    username = get_current_username(credentials)

    assert username == "denis"


def test_get_current_username_from_invalid_token():
    """
    Проверяет, что неверный токен вызывает код ошибки 401.
    """
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="invalid-token",
    )

    with pytest.raises(HTTPException) as error:
        get_current_username(credentials)

    assert error.value.status_code == 401


def test_get_current_username_without_sub():
    """
    Проверяет, что токен без поля sub вызывает код ошибки 401.
    """
    token = create_access_token({"data": "test"})

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    with pytest.raises(HTTPException) as error:
        get_current_username(credentials)

    assert error.value.status_code == 401
