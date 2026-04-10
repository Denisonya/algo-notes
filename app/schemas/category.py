from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    """
    Base schema for Category.
    """
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Category name"
    )

    model_config = ConfigDict(
        from_attributes=True  # ORM mode (Pydantic преобразует SQLAlchemy‑объекты в JSON‑совместимые словари)
    )


class CategoryCreate(CategoryBase):
    """
    Schema for creating a category.
    Inherits all fields from CategoryBase.
    """
    pass


class CategoryUpdate(CategoryBase):
    """
    Schema for updating a category.
    Requires all fields to be present.
    """
    pass


class CategoryPatch(BaseModel):
    """
    Schema for partial updating a category.
    All fields are optional.
    """
    name: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Optional category name"
    )

    model_config = ConfigDict(from_attributes=True)


class CategoryRead(CategoryBase):
    """
    Schema for reading category data.
    """
    id: int
