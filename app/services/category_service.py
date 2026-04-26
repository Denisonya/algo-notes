from sqlalchemy.orm import Session

from ..models import Category, User
from ..schemas.category import CategoryCreate, CategoryUpdate, CategoryPatch
from ..core.exceptions import NotFoundError, AlreadyExistsError
from ..utils.common import apply_updates

from ..repositories.category_repository import (
    get_all_categories_by_user,
    get_category_by_id,
    get_category_by_name_for_user,
    create_category,
    update_category,
    delete_category,
)


def get_all_categories_service(db: Session, user: User) -> list[Category]:
    """
    Retrieve all categories belonging to current user.

    :param db: Database session
    :param user: Current authenticated user
    :return: List of Category objects
    """
    return get_all_categories_by_user(db, user.id)


def get_category_by_id_service(category_id: int, db: Session, user: User) -> Category:
    """
    Retrieve category by ID.

    :param category_id: Category ID
    :param db: Database session
    :param user: Current authenticated user
    :return: Category object
    """
    category = get_category_by_id(db, category_id)

    if category is None or category.user_id != user.id:
        raise NotFoundError("Category not found")

    return category


def create_category_service(data: CategoryCreate, db: Session, user: User) -> Category:
    """
    Create a new category.

    :param data: CategoryCreate schema
    :param db: Database session
    :param user: Current authenticated user
    :return: Created Category object
    """
    if get_category_by_name_for_user(db, data.name, user.id):
        raise AlreadyExistsError("Category already exists")

    category = Category(
        **data.model_dump(),
        user_id=user.id
    )

    try:
        create_category(db, category)
        db.commit()
        db.refresh(category)
        return category
    except Exception:
        db.rollback()
        raise


def update_category_service(category_id: int, data: CategoryUpdate, db: Session, user: User) -> Category:
    """
    Update category.

    :param category_id: Category ID
    :param data: CategoryUpdate schema
    :param db: Database session
    :param user: Current authenticated user
    :return: Updated Category object
    """
    category = get_category_by_id(db, category_id)

    if category is None or category.user_id != user.id:
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


def patch_category_service(category_id: int, data: CategoryPatch, db: Session, user: User) -> Category:
    """
    Partially update category.

    :param category_id: Category ID
    :param data: CategoryPatch schema
    :param db: Database session
    :param user: Current authenticated user
    :return: Updated Category object
    """
    category = get_category_by_id(db, category_id)

    if category is None or category.user_id != user.id:
        raise NotFoundError("Category not found")

    try:
        apply_updates(category, data.model_dump(exclude_unset=True))
        update_category(db, category)
        db.commit()
        db.refresh(category)
        return category
    except Exception:
        db.rollback()
        raise


def delete_category_service(category_id: int, db: Session, user: User) -> None:
    """
    Delete category.

    :param category_id: Category ID
    :param db: Database session
    :param user: Current authenticated user
    :return: None
    """
    category = get_category_by_id(db, category_id)

    if category is None or category.user_id != user.id:
        raise NotFoundError("Category not found")

    try:
        delete_category(db, category)
        db.commit()
    except Exception:
        db.rollback()
        raise