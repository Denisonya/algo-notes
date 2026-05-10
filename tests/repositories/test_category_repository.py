from sqlalchemy.orm import Session

from app.models import Category, User
from app.repositories.category_repository import (
    create_category,
    delete_category,
    get_all_categories,
    get_all_categories_by_user,
    get_category_by_id,
    get_category_by_name_for_user,
    update_category,
)


def test_create_category(db: Session, user: User):
    """
    Проверяет, что категорию можно создать.
    """
    category = Category(
        name="Graphs",
        user_id=user.id,
    )

    create_category(db, category)
    db.commit()
    db.refresh(category)

    assert category.id is not None
    assert category.name == "Graphs"
    assert category.user_id == user.id


def test_get_category_by_id(db: Session, user: User):
    """
    Проверяет, что категорию можно найти по id.
    """
    category = Category(
        name="Graphs",
        user_id=user.id,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    result = get_category_by_id(db, category.id)

    assert result is not None
    assert result.name == "Graphs"


def test_get_all_categories(db: Session, user: User):
    """
    Проверяет, что можно получить все категории.
    """
    db.add_all(
        [
            Category(name="Graphs", user_id=user.id),
            Category(name="Sorting", user_id=user.id),
        ]
    )
    db.commit()

    categories = get_all_categories(db)

    assert len(categories) == 2


def test_get_all_categories_by_user(db: Session, user: User):
    """
    Проверяет, что можно получить категории конкретного пользователя.
    """
    db.add_all(
        [
            Category(name="Graphs", user_id=user.id),
            Category(name="Sorting", user_id=user.id),
        ]
    )
    db.commit()

    categories = get_all_categories_by_user(db, user.id)

    assert len(categories) == 2
    assert categories[0].user_id == user.id


def test_get_category_by_name_for_user(db: Session, user: User):
    """
    Проверяет, что категорию можно найти по имени и id пользователя.
    """
    category = Category(
        name="Graphs",
        user_id=user.id,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    result = get_category_by_name_for_user(
        db,
        "Graphs",
        user.id,
    )

    assert result is not None
    assert result.id == category.id


def test_update_category(db: Session, user: User):
    """
    Проверяет, что категорию можно обновить.
    """
    category = Category(
        name="Graphs",
        user_id=user.id,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    category.name = "Sorting"

    update_category(db, category)
    db.commit()
    db.refresh(category)

    assert category.name == "Sorting"


def test_delete_category(db: Session, user: User):
    """
    Проверяет, что категорию можно удалить.
    """
    category = Category(
        name="Graphs",
        user_id=user.id,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    category_id = category.id

    delete_category(db, category)
    db.commit()

    assert get_category_by_id(db, category_id) is None