import pytest

from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.category_service import (
    create_category_service,
    get_category_by_id_service,
    update_category_service,
)
from app.core.exceptions import NotFoundError, AlreadyExistsError


def test_create_category_service(db):
    data = CategoryCreate(name="Graphs")

    category = create_category_service(data, db)

    assert category.id is not None
    assert category.name == "Graphs"


def test_create_category_duplicate(db):
    data = CategoryCreate(name="Graphs")

    create_category_service(data, db)

    with pytest.raises(AlreadyExistsError):
        create_category_service(data, db)


def test_get_category_not_found(db):
    with pytest.raises(NotFoundError):
        get_category_by_id_service(1000, db)


def test_update_category(db):
    data = CategoryCreate(name="Graphs")
    category = create_category_service(data, db)

    updated = update_category_service(
        category.id,
        CategoryUpdate(name="Sorting"),
        db
    )

    assert updated.name == "Sorting"
