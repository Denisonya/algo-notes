from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import category
from ..services import category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=category.CategoryResponse)
def create_category(data: category.CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new category
    :param data: Pydantic model with category fields (name)
    :param db: database session
    :return: created category
    """
    return category_service.create_category(db, data)


@router.get("/", response_model=list[category.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """
    Get all categories
    :return: list of categories
    """
    return category_service.get_all_categories(db)
