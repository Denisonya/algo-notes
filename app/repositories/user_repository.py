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


def create_user(db: Session, user: User) -> User:
    """
    Create new user (add to session, not committed).

    :param db: Database session
    :param user: User object
    :return: Created User object
    """
    db.add(user)
    db.flush()
    return user
