from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


# Делаем связь Category.notes <-> Note.category

# Модель категории, объекты которой будут храниться в БД
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    notes = relationship("Note", back_populates="category",
                         cascade="all, delete-orphan")  # связь с моделью Note через ее атрибут category


# Модель заметки, объекты которой будут храниться в БД
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"))  # внешний ключ на столбец id из таблицы "categories"
    category = relationship("Category", back_populates="notes")  # связь с моделью Category через ее атрибут notes

# Примечание:
# Параметр back_populates представляет атрибут связанной модели, с которой будет сопоставляться текущая модель
