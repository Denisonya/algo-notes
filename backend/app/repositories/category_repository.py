from sqlalchemy.orm import Session
from ..models.category import Category


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
    return db.query(Category).get(category_id)


def get_all(db: Session) -> list[Category]:
    """
    Retrieve all categories.

    :param db: Database session
    :return: List of categories
    """
    return db.query(Category).all()
