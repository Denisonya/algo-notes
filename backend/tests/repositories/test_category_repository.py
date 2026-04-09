from ...app.repositories import category_repository


def test_create_category(db):
    category = category_repository.create(db, "Graph")

    assert category.id is not None
    assert category.name == "Graph"


def test_get_all_categories(db):
    category_repository.create(db, "Graph")
    category_repository.create(db, "DP")

    categories = category_repository.get_all(db)

    assert len(categories) == 2


def test_get_category_by_id(db):
    category = category_repository.create(db, "Graph")

    found = category_repository.get_by_id(db, category.id)

    assert found is not None
    assert found.id == category.id
