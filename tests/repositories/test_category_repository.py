from app.repositories import category_repository


def test_create_category(db):
    created = category_repository.create(db, "Graphs")

    assert created.id is not None
    assert created.name == "Graphs"


def test_get_all_categories(db):
    category_repository.create(db, "Graphs")
    category_repository.create(db, "Sorting")

    created = category_repository.get_all(db)

    assert len(created) == 2


def test_get_category_by_id(db):
    created = category_repository.create(db, "Graphs")

    fetched = category_repository.get_by_id(db, created.id)

    assert fetched is not None
    assert fetched.id == created.id
