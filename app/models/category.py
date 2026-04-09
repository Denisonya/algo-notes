from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


# Связь Category -> Note (1:N)


# Модель категории, объекты которой будут храниться в БД
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    notes: Mapped[list["Note"]] = relationship(  # type: ignore
        "Note",
        back_populates="category",  # связь с моделью Note через ее атрибут category
        cascade="all, delete-orphan"
    )

# Примечание:
# Параметр back_populates представляет атрибут связанной модели, с которой будет сопоставляться текущая модель
