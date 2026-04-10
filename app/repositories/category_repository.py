from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Category


def get_all_categories(db: Session) -> list[Category]:
    """
    Retrieve all categories ordered by ID.

    :param db: Database session
    :return: List of Category objects
    """
    stmt = select(Category).order_by(Category.id)
    result = db.execute(stmt)
    return result.scalars().all()  # type: ignore


def get_category_by_id(db: Session, category_id: int) -> Category | None:
    """
    Get category by its ID.

    :param db: Database session
    :param category_id: Category ID
    :return: Category object or None
    """
    stmt = select(Category).where(Category.id == category_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def get_category_by_name(db: Session, name: str) -> Category | None:
    """
    Get category by name.

    :param db: Database session
    :param name: Category name
    :return: Category object or None
    """
    stmt = select(Category).where(Category.name == name)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def create_category(db: Session, category: Category) -> Category:
    """
    Add a new category to the session and flush changes.

    :param db: Database session
    :param category: Category object
    :return: Category object (not committed)
    """
    db.add(category)
    db.flush()
    return category


def update_category(db: Session, category: Category) -> Category:
    """
    Flush updated category to the database.

    :param db: Database session
    :param category: Category object
    :return: Updated Category object
    """
    db.flush()
    return category


def delete_category(db: Session, category: Category) -> Category:
    """
    Delete category from session.

    :param db: Database session
    :param category: Category object
    :return: Deleted Category object
    """
    db.delete(category)
    return category
