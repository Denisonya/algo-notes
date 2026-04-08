from sqlalchemy.orm import Session
from ..models import Category
from .. import schemas


def create_category(db: Session, category_data: schemas.CategoryCreate):
    """
    Create a new category
    :param category_data: Pydantic model with category fields (name)
    :param db: database session
    :return: created category
    """
    category = Category(name=category_data.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_categories(db: Session):
    """
    Get all categories
    :return: list of categories
    """
    return db.query(Category).all()
