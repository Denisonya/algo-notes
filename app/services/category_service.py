from sqlalchemy.orm import Session

from ..models import Category
from ..schemas.category import CategoryCreate, CategoryUpdate, CategoryPatch
from ..core.exceptions import NotFoundError, AlreadyExistsError
from ..utils.common import apply_updates

from ..repositories.category_repository import (
    get_all_categories,
    get_category_by_id,
    get_category_by_name,
    create_category,
    update_category,
    delete_category,
)


def get_all_categories_service(db: Session) -> list[Category]:
    """
    Retrieve all categories.

    :param db: Database session
    :return: List of Category objects
    """
    return get_all_categories(db)


def get_category_by_id_service(category_id: int, db: Session) -> Category:
    """
    Retrieve category by ID.

    :param category_id: Category ID
    :param db: Database session
    :return: Category object
    :raises NotFoundError: If category not found
    """
    category = get_category_by_id(db, category_id)

    if category is None:
        raise NotFoundError("Category not found")

    return category


def create_category_service(data: CategoryCreate, db: Session) -> Category:
    """
    Create a new category.

    :param data: CategoryCreate schema
    :param db: Database session
    :return: Created Category object
    :raises AlreadyExistsError: If category already exists
    """
    if get_category_by_name(db, data.name):
        raise AlreadyExistsError("Category already exists")

    category = Category(**data.model_dump())

    try:
        create_category(db, category)
        db.commit()
        db.refresh(category)
        return category
    except Exception:
        db.rollback()
        raise


def update_category_service(category_id: int, data: CategoryUpdate, db: Session) -> Category:
    """
    Update category.

    :param category_id: Category ID
    :param data: CategoryUpdate schema
    :param db: Database session
    :return: Updated Category object
    :raises NotFoundError: If category not found
    """
    category = get_category_by_id(db, category_id)

    if category is None:
        raise NotFoundError("Category not found")

    try:
        category.name = data.name

        update_category(db, category)
        db.commit()
        db.refresh(category)

        return category
    except Exception:
        db.rollback()
        raise


def patch_category_service(category_id: int, data: CategoryPatch, db: Session) -> Category:
    """
    Partial update category.

    :param category_id: Category ID
    :param data: CategoryPatch schema
    :param db: Database session
    :return: Partial updated Category object
    :raises NotFoundError: If category not found
    """
    category = get_category_by_id(db, category_id)

    if category is None:
        raise NotFoundError("Category not found")

    try:
        apply_updates(category, data.model_dump(
            exclude_unset=True))  # exclude_unset - передаем словарь только с измененными полями (поля, которые не были переданы, остаются прежними)

        update_category(db, category)
        db.commit()
        db.refresh(category)

        return category
    except Exception:
        db.rollback()
        raise


def delete_category_service(category_id: int, db: Session) -> None:
    """
    Delete category.

    :param category_id: Category ID
    :param db: Database session
    :return: None
    :raises NotFoundError: If category not found
    """
    category = get_category_by_id(db, category_id)

    if category is None:
        raise NotFoundError("Category not found")

    try:
        delete_category(db, category)
        db.commit()
    except Exception:
        db.rollback()
        raise
