from pydantic import BaseModel, Field
from typing import Optional


# Модели для категорий
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Название категории")


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # режим ORM, чтобы Pydantic мог преобразовывать SQLAlchemy‑объекты в JSON‑совместимые словари


# Модели для заметок
class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Заголовок заметки")
    content: str = Field(..., min_length=1, description="Содержание заметки")
    category_id: int = Field(..., ge=1, description="ID категории")


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    category_id: int
    category: Optional[CategoryResponse] = None  # вложенная модель для связи c моделью категорий

    class Config:
        from_attributes = True  # режим ORM, чтобы Pydantic мог преобразовывать SQLAlchemy‑объекты в JSON‑совместимые словари
