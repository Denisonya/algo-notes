from sqlalchemy.orm import Session

from app.models import User
from app.repositories.user_repository import (
    create_user,
    get_user_by_id,
    get_user_by_username,
)


def test_create_user(db: Session):
    """
    Проверяет, что пользователя можно создать.
    """
    user = User(
        username="denis",
        hashed_password="2006",
    )

    create_user(db, user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.username == "denis"


def test_get_user_by_username(db: Session):
    """
    Проверяет, что пользователя можно найти по username.
    """
    user = User(
        username="denis",
        hashed_password="2006",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    result = get_user_by_username(db, "denis")

    assert result is not None
    assert result.username == "denis"


def test_get_user_by_id(db: Session):
    """
    Проверяет, что пользователя можно найти по id.
    """
    user = User(
        username="denis",
        hashed_password="2006",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    result = get_user_by_id(db, user.id)

    assert result is not None
    assert result.id == user.id


def test_get_missing_user_returns_none(db: Session):
    """
    Проверяет, что для несуществующего пользователя возвращается None.
    """
    result = get_user_by_username(db, "missing-user")

    assert result is None
