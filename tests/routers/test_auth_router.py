from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    """
    Проверяет эндпоинт регистрации пользователя.
    """
    response = client.post(
        "/auth/register",
        json={
            "username": "denis",
            "password": "2006",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["username"] == "denis"
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_user(client: TestClient):
    """
    Проверяет, что повторная регистрация возвращает код ошибки 409.
    """
    client.post(
        "/auth/register",
        json={
            "username": "denis",
            "password": "2006",
        },
    )

    response = client.post(
        "/auth/register",
        json={
            "username": "denis",
            "password": "2006",
        },
    )

    assert response.status_code == 409


def test_login_user(client: TestClient):
    """
    Проверяет вход пользователя с правильными данными.
    """
    client.post(
        "/auth/register",
        json={
            "username": "denis",
            "password": "2006",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "denis",
            "password": "2006",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient):
    """
    Проверяет, что вход с неправильным паролем возвращает код ошибки 401.
    """
    client.post(
        "/auth/register",
        json={
            "username": "denis",
            "password": "2006",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "denis",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401


def test_login_missing_user(client: TestClient):
    """
    Проверяет, что вход несуществующего пользователя возвращает код ошибки401.
    """
    response = client.post(
        "/auth/login",
        json={
            "username": "missing-user",
            "password": "missing-password",
        },
    )

    assert response.status_code == 401