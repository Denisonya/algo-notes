from fastapi.testclient import TestClient


def test_notes_require_auth(client: TestClient):
    """
    Проверяет, что эндпоинт заметок требует авторизацию.
    """
    response = client.get("/notes/")

    assert response.status_code in (401, 403)


def test_create_note(client: TestClient, auth_headers: dict[str, str]):
    """
    Проверяет создание заметки через API.
    """
    category_response = client.post(
        "/categories/",
        json={"name": "Graphs"},
        headers=auth_headers,
    )

    category_id = category_response.json()["id"]

    response = client.post(
        "/notes/",
        json={
            "title": "DFS",
            "content": "Test",
            "category_id": category_id,
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "DFS"
    assert data["content"] == "Test"
    assert data["category_id"] == category_id


def test_create_note_in_missing_category_returns_404(
        client: TestClient,
        auth_headers: dict[str, str],
):
    """
    Проверяет, что нельзя создать заметку в несуществующей категории.
    """
    response = client.post(
        "/notes/",
        json={
            "title": "DFS",
            "content": "Test",
            "category_id": 1000,
        },
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_get_all_notes(client: TestClient, auth_headers: dict[str, str]):
    """
    Проверяет получение всех заметок текущего пользователя.
    """
    category_response = client.post(
        "/categories/",
        json={"name": "Graphs"},
        headers=auth_headers,
    )

    category_id = category_response.json()["id"]

    client.post(
        "/notes/",
        json={
            "title": "DFS",
            "content": "Test1",
            "category_id": category_id,
        },
        headers=auth_headers,
    )

    client.post(
        "/notes/",
        json={
            "title": "BFS",
            "content": "Test2",
            "category_id": category_id,
        },
        headers=auth_headers,
    )

    response = client.get(
        "/notes/",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_note_by_id(client: TestClient, auth_headers: dict[str, str]):
    """
    Проверяет получение заметки по id.
    """
    category_response = client.post(
        "/categories/",
        json={"name": "Graphs"},
        headers=auth_headers,
    )

    category_id = category_response.json()["id"]

    create_response = client.post(
        "/notes/",
        json={
            "title": "DFS",
            "content": "Test",
            "category_id": category_id,
        },
        headers=auth_headers,
    )

    note_id = create_response.json()["id"]

    response = client.get(
        f"/notes/{note_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == note_id
    assert response.json()["title"] == "DFS"


def test_get_missing_note_returns_404(
        client: TestClient,
        auth_headers: dict[str, str],
):
    """
    Проверяет, что для несуществующей заметки возвращается код ошибки 404.
    """
    response = client.get(
        "/notes/1000",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_get_notes_by_category_id(
        client: TestClient,
        auth_headers: dict[str, str],
):
    """
    Проверяет получение заметок по id категории.
    """
    category_response = client.post(
        "/categories/",
        json={"name": "Graphs"},
        headers=auth_headers,
    )

    category_id = category_response.json()["id"]

    client.post(
        "/notes/",
        json={
            "title": "DFS",
            "content": "Test1",
            "category_id": category_id,
        },
        headers=auth_headers,
    )

    response = client.get(
        f"/notes/category/{category_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_note(client: TestClient, auth_headers: dict[str, str]):
    """
    Проверяет полное обновление заметки.
    """
    category_response = client.post(
        "/categories/",
        json={"name": "Graphs"},
        headers=auth_headers,
    )

    category_id = category_response.json()["id"]

    create_response = client.post(
        "/notes/",
        json={
            "title": "DFS",
            "content": "Test",
            "category_id": category_id,
        },
        headers=auth_headers,
    )

    note_id = create_response.json()["id"]

    response = client.put(
        f"/notes/{note_id}",
        json={
            "title": "BFS",
            "content": "Updated content",
            "category_id": category_id,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["title"] == "BFS"
    assert response.json()["content"] == "Updated content"


def test_patch_note(client: TestClient, auth_headers: dict[str, str]):
    """
    Проверяет частичное обновление заметки.
    """
    category_response = client.post(
        "/categories/",
        json={"name": "Graphs"},
        headers=auth_headers,
    )

    category_id = category_response.json()["id"]

    create_response = client.post(
        "/notes/",
        json={
            "title": "DFS",
            "content": "Test",
            "category_id": category_id,
        },
        headers=auth_headers,
    )

    note_id = create_response.json()["id"]

    response = client.patch(
        f"/notes/{note_id}",
        json={"content": "Patched content"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["content"] == "Patched content"


def test_delete_note(client: TestClient, auth_headers: dict[str, str]):
    """
    Проверяет удаление заметки.
    """
    category_response = client.post(
        "/categories/",
        json={"name": "Graphs"},
        headers=auth_headers,
    )

    category_id = category_response.json()["id"]

    create_response = client.post(
        "/notes/",
        json={
            "title": "DFS",
            "content": "Test",
            "category_id": category_id,
        },
        headers=auth_headers,
    )

    note_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/notes/{note_id}",
        headers=auth_headers,
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/notes/{note_id}",
        headers=auth_headers,
    )

    assert get_response.status_code == 404
