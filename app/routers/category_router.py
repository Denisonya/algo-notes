from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate, CategoryPatch
from app.services.category_service import (
    get_all_categories_service,
    get_category_by_id_service,
    create_category_service,
    update_category_service,
    patch_category_service,
    delete_category_service,
)
from app.core.exceptions import NotFoundError, AlreadyExistsError

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryRead])
def get_all_categories(db: Session = Depends(get_db)):
    try:
        return get_all_categories_service(db)
    except SQLAlchemyError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "DB error")


@router.get("/{category_id}", response_model=CategoryRead)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    try:
        return get_category_by_id_service(category_id, db)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return create_category_service(data, db)
    except AlreadyExistsError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db)):
    try:
        return update_category_service(category_id, data, db)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.patch("/{category_id}", response_model=CategoryRead)
def patch_category(category_id: int, data: CategoryPatch, db: Session = Depends(get_db)):
    try:
        return patch_category_service(category_id, data, db)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        delete_category_service(category_id, db)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
    except SQLAlchemyError:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "DB error")
