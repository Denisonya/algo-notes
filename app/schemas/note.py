from pydantic import BaseModel, ConfigDict, Field
from .category import CategoryRead


class NoteBase(BaseModel):
    """
    Base schema for Note.
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Note title"
    )
    content: str = Field(
        ...,
        min_length=1,
        description="Note content"
    )

    model_config = ConfigDict(
        from_attributes=True  # ORM mode (Pydantic преобразует SQLAlchemy‑объекты в JSON‑совместимые словари)
    )


class NoteCreate(NoteBase):
    """
    Schema for creating a note.
    Requires all fields from NoteBase plus category_id.
    """
    category_id: int = Field(
        ...,
        ge=1,
        description="Category ID"
    )


class NoteUpdate(NoteCreate):
    """
    Schema for updating a note.
    Requires all fields to be present.
    Inherits from NoteCreate to avoid duplication.
    """
    pass


class NotePatch(BaseModel):
    """
    Schema for partial updating a note.
    All fields are optional.
    """
    title: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Optional note title"
    )
    content: str | None = Field(
        None,
        min_length=1,
        description="Optional note content"
    )
    category_id: int | None = Field(
        None,
        ge=1,
        description="Optional category ID"
    )

    model_config = ConfigDict(from_attributes=True)


class NoteRead(NoteBase):
    """
    Schema for reading note data.
    """
    id: int
    category_id: int
    category: CategoryRead | None = None  # вложенная модель для связи c моделью категорий
