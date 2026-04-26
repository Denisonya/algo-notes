from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


# Связь User -> Category (1:N)
# Связь User -> Note (1:N)

# Модель пользователя, объекты которой будут храниться в БД
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    categories: Mapped[list["Category"]] = relationship(  # type: ignore
        "Category",
        back_populates="user",  # связь с моделью Category через ее атрибут category
        cascade="all, delete-orphan"
    )

    notes: Mapped[list["Note"]] = relationship(  # type: ignore
        "Note",
        back_populates="user",  # связь с моделью Note через ее атрибут user
        cascade="all, delete-orphan"
    )

# Примечание:
# Параметр back_populates представляет атрибут связанной модели, с которой будет сопоставляться текущая модель