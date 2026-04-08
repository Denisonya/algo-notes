from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


# Делаем связь Category.notes <-> Note.category

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
