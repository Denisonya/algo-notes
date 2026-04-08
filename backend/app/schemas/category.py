from pydantic import BaseModel, Field


# Модели для категорий
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Название категории")


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # режим ORM, чтобы Pydantic мог преобразовывать SQLAlchemy‑объекты в JSON‑совместимые словари
