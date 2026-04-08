from sqlalchemy.orm import Session
from ..repositories import category_repository
from ..schemas import category as category_schema


def create_category(db: Session, data: category_schema.CategoryCreate):
    """
    Create a new category
    :param data: Pydantic model with category fields (name)
    :param db: database session
    :return: created category
    """
    return category_repository.create(db, data.name)


def get_all_categories(db: Session):
    """
    Get all categories
    :return: list of categories
    """
    return category_repository.get_all(db)
