from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base import Base


# Связь Category -> Note (1:N)

# Модель заметки, объекты которой будут храниться в БД
class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    content: Mapped[str] = mapped_column(String, nullable=False)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),  # внешний ключ на столбец id из таблицы "categories"
        nullable=False,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),  # внешний ключ на столбец id из таблицы "users"
        nullable=False,
        index=True
    )

    category: Mapped["Category"] = relationship(  # type: ignore
        "Category",
        back_populates="notes"  # связь с моделью Category через ее атрибут notes
    )

    user: Mapped["User"] = relationship(  # type: ignore
        "User",
        back_populates="notes"  # связь с моделью User через ее атрибут notes
    )

# Примечание:
# Параметр back_populates представляет атрибут связанной модели, с которой будет сопоставляться текущая модель