from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Get user by username.

    :param db: Database session
    :param username: Username
    :return: User object or None
    """
    stmt = select(User).where(User.username == username)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Get user by ID.

    :param db: Database session
    :param user_id: User ID
    :return: User object or None
    """
    stmt = select(User).where(User.id == user_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def create_user(db: Session, user: User) -> User:
    """
    Create new user (not committed).

    :param db: Database session
    :param user: User object
    :return: Created user
    """
    db.add(user)
    db.flush()
    return user