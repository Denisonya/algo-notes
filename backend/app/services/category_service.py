from sqlalchemy.orm import Session
from ..repositories import category_repository
from ..schemas import category as category_schema
from ..models.category import Category


def create_category(db: Session, data: category_schema.CategoryCreate) -> Category:
    """
    Create a new category.

    :param db: Database session
    :param data: Category input data
    :return: Created Category object
    """
    return category_repository.create(db, data.name)


def get_all_categories(db: Session) -> list[Category]:
    """
    Retrieve all categories.

    :param db: Database session
    :return: List of categories
    """
    return category_repository.get_all(db)
