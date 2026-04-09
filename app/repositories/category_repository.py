from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import Category


def create(db: Session, name: str) -> Category:
    """
    Create a new category.

    :param db: Database session
    :param name: Category name
    :return: Created Category object
    """
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_by_id(db: Session, category_id: int) -> Category | None:
    """
    Get category by its ID.

    :param db: Database session
    :param category_id: Category ID
    :return: Category object or None
    """
    stmt = select(Category).where(Category.id == category_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def get_all(db: Session) -> list[Category]:
    """
    Retrieve all categories.

    :param db: Database session
    :return: List of categories
    """
    stmt = select(Category)
    result = db.execute(stmt)
    return result.scalars().all()  # type: ignore
