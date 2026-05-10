import pytest
from sqlalchemy.orm import Session

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.models import Category, User
from app.schemas.category import CategoryCreate, CategoryPatch, CategoryUpdate
from app.services.category_service import (
    create_category_service,
    delete_category_service,
    get_all_categories_service,
    get_category_by_id_service,
    patch_category_service,
    update_category_service,
)


def test_create_category_service(db: Session, user: User):
    """
    Проверяет, что сервис создает категорию для текущего пользователя.
    """
    data = CategoryCreate(name="Graphs")

    category = create_category_service(data, db, user)

    assert category.id is not None
    assert category.name == "Graphs"
    assert category.user_id == user.id


def test_create_category_duplicate(db: Session, user: User):
    """
    Проверяет, что пользователь не может создать две категории с одинаковым именем.
    """
    data = CategoryCreate(name="Graphs")

    create_category_service(data, db, user)

    with pytest.raises(AlreadyExistsError):
        create_category_service(data, db, user)


def test_get_all_categories_service(db: Session, user: User):
    """
    Проверяет, что сервис возвращает все категории текущего пользователя.
    """
    create_category_service(
        CategoryCreate(name="Graphs"),
        db,
        user,
    )

    create_category_service(
        CategoryCreate(name="Sorting"),
        db,
        user,
    )

    categories = get_all_categories_service(db, user)

    assert len(categories) == 2


def test_get_category_by_id_service(db: Session, user: User):
    """
    Проверяет, что сервис возвращает категорию по id.
    """
    category = create_category_service(
        CategoryCreate(name="Graphs"),
        db,
        user,
    )

    result = get_category_by_id_service(category.id, db, user)

    assert result.id == category.id
    assert result.name == "Graphs"


def test_get_category_not_found(db: Session, user: User):
    """
    Проверяет, что для несуществующей категории возникает NotFoundError.
    """
    with pytest.raises(NotFoundError):
        get_category_by_id_service(1000, db, user)


def test_user_cannot_get_foreign_category(db: Session, user: User):
    """
    Проверяет, что пользователь не может получить чужую категорию.
    """
    another_user = User(
        username="alex",
        hashed_password="2000",
    )

    db.add(another_user)
    db.commit()
    db.refresh(another_user)

    foreign_category = Category(
        name="Foreign",
        user_id=another_user.id,
    )

    db.add(foreign_category)
    db.commit()
    db.refresh(foreign_category)

    with pytest.raises(NotFoundError):
        get_category_by_id_service(foreign_category.id, db, user)


def test_update_category(db: Session, user: User):
    """
    Проверяет, что сервис полностью обновляет категорию.
    """
    category = create_category_service(
        CategoryCreate(name="Graphs"),
        db,
        user,
    )

    updated = update_category_service(
        category.id,
        CategoryUpdate(name="Sorting"),
        db,
        user,
    )

    assert updated.name == "Sorting"


def test_patch_category(db: Session, user: User):
    """
    Проверяет, что сервис частично обновляет категорию.
    """
    category = create_category_service(
        CategoryCreate(name="Graphs"),
        db,
        user,
    )

    patched = patch_category_service(
        category.id,
        CategoryPatch(name="Algorithms"),
        db,
        user,
    )

    assert patched.name == "Algorithms"


def test_delete_category(db: Session, user: User):
    """
    Проверяет, что сервис удаляет категорию.
    """
    category = create_category_service(
        CategoryCreate(name="Graphs"),
        db,
        user,
    )

    category_id = category.id

    delete_category_service(category_id, db, user)

    with pytest.raises(NotFoundError):
        get_category_by_id_service(category_id, db, user)