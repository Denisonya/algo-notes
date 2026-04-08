from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas
from ..services import category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=schemas.CategoryResponse)
def create_category(category_data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new category
    :param category_data: Pydantic model with category fields (name)
    :param db: database session
    :return: created category
    """
    return category_service.create_category(db, category_data)


@router.get("/", response_model=list[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """
    Get all categories
    :return: list of categories
    """
    return category_service.get_categories(db)
