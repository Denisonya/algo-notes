from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base


# Делаем связь Category.notes <-> Note.category

# Модель категории, объекты которой будут храниться в БД
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    notes = relationship(
        "Note",
        back_populates="category",  # связь с моделью Note через ее атрибут category
        cascade="all, delete-orphan"
    )
