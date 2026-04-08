from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import category
from ..services import category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=category.CategoryResponse)
def create_category(data: category.CategoryCreate, db: Session = Depends(get_db)) -> category.CategoryResponse:
    """
    Create a new category.

    :param data: Category input data
    :param db: Database session
    :return: Created category
    """
    return category_service.create_category(db, data)


@router.get("/", response_model=list[category.CategoryResponse])
def get_categories(db: Session = Depends(get_db)) -> list[category.CategoryResponse]:
    """
    Retrieve all categories.

    :param db: Database session
    :return: List of categories
    """
    return category_service.get_all_categories(db)
