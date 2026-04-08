from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


# параметр back_populates представляет атрибут связанной модели, с которой будет сопоставляться текущая модель
# делаем связь Category.notes -- Note.category

# создаем модель категории, объекты которой будут храниться в бд
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    notes = relationship("Note", back_populates="category",
                         cascade="all, delete-orphan")  # связь с моделью Note через ее атрибут category


# создаем модель заметки, объекты которой будут храниться в бд
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"))  # внешний ключ на столбец id из таблицы "categories"
    category = relationship("Category", back_populates="notes")  # связь с моделью Category через ее атрибут notes
