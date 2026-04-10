from app.models import Category
from app.repositories.category_repository import (
    create_category,
    get_category_by_id,
    get_all_categories,
    delete_category,
)


def test_create_category(db):
    category = Category(name="Graphs")

    create_category(db, category)
    db.commit()

    assert category.id is not None


def test_get_category_by_id(db):
    category = Category(name="Graphs")
    db.add(category)
    db.commit()

    result = get_category_by_id(db, category.id)

    assert result is not None
    assert result.name == "Graphs"


def test_get_all_categories(db):
    db.add_all([
        Category(name="Graphs"),
        Category(name="Sorting"),
    ])
    db.commit()

    categories = get_all_categories(db)

    assert len(categories) == 2


def test_delete_category(db):
    category = Category(name="Graphs")
    db.add(category)
    db.commit()

    delete_category(db, category)
    db.commit()

    assert get_category_by_id(db, category.id) is None
