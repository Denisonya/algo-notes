from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    categories: Mapped[list["Category"]] = relationship(  # type: ignore
        "Category",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    notes: Mapped[list["Note"]] = relationship(  # type: ignore
        "Note",
        back_populates="user",
        cascade="all, delete-orphan"
    )
