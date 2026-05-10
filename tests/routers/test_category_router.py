from fastapi.testclient import TestClient


def test_categories_require_auth(client: TestClient):
    """
    Проверяет, что эндпоинт категорий требует авторизацию.
    """
    response = client.get("/categories/")

    assert response.status_code in (401, 403)


def test_create_category(client: TestClient, auth_headers: dict[str, str]):
    """
    Проверяет создание категории через API.
    """
    response = client.post(
        "/categories/",
        json={"name": "Graphs"},
        headers=auth_headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["name"] == "Graphs"


def test_get_all_categories(client: TestClient, auth_headers: dict[str, str]):
    """
    Проверяет получение всех категорий текущего пользователя.
    """
    client.post(
        "/categories/",
        json={"name": "Graphs"},
        headers=auth_headers,
    )

    client.post(
        "/categories/",
        json={"name": "Sorting"},
        headers=auth_headers,
    )

    response = client.get(
        "/categories/",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_category_by_id(client: TestClient, auth_headers: dict[str, str]):
    """
    Проверяет получение категории по id.
    """
    create_response = client.post(
        "/categories/",
        json={"name": "Graphs"},
        headers=auth_headers,
    )

    category_id = create_response.json()["id"]

    response = client.get(
        f"/categories/{category_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == category_id
    assert response.json()["name"] == "Graphs"


def test_get_missing_category_returns_404(
    client: TestClient,
    auth_headers: dict[str, str],
):
    """
    Проверяет, что для несуществующей категории возвращается 404.
    """
    response = client.get(
        "/categories/1000",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_create_duplicate_category_returns_409(
    client: TestClient,
    auth_headers: dict[str, str],
):
    """
    Проверяет, что дубликат категории возвращает 409.
    """
    client.post(
        "/categories/",
        json={"name": "Graphs"},
        headers=auth_headers,
    )

    response = client.post(
        "/categories/",
        json={"name": "Graphs"},
        headers=auth_headers,
    )

    assert response.status_code == 409


def test_update_category(client: TestClient, auth_headers: dict[str, str]):
    """
    Проверяет полное обновление категории.
    """
    create_response = client.post(
        "/categories/",
        json={"name": "Graphs"},
        headers=auth_headers,
    )

    category_id = create_response.json()["id"]

    response = client.put(
        f"/categories/{category_id}",
        json={"name": "Sorting"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Sorting"


def test_patch_category(client: TestClient, auth_headers: dict[str, str]):
    """
    Проверяет частичное обновление категории.
    """
    create_response = client.post(
        "/categories/",
        json={"name": "Graphs"},
        headers=auth_headers,
    )

    category_id = create_response.json()["id"]

    response = client.patch(
        f"/categories/{category_id}",
        json={"name": "Algorithms"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Algorithms"


def test_delete_category(client: TestClient, auth_headers: dict[str, str]):
    """
    Проверяет удаление категории.
    """
    create_response = client.post(
        "/categories/",
        json={"name": "Graphs"},
        headers=auth_headers,
    )

    category_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/categories/{category_id}",
        headers=auth_headers,
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/categories/{category_id}",
        headers=auth_headers,
    )

    assert get_response.status_code == 404