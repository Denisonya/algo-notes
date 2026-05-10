from sqlalchemy.orm import Session

from app.models import Category, Note, User
from app.repositories.note_repository import (
    create_note,
    delete_note,
    get_all_notes,
    get_all_notes_by_user,
    get_note_by_id,
    get_notes_by_category_id,
    update_note,
)


def test_create_note(db: Session, user: User):
    """
    Проверяет, что заметку можно создать.
    """
    category = Category(
        name="Graphs",
        user_id=user.id,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    note = Note(
        title="DFS",
        content="Test",
        category_id=category.id,
        user_id=user.id,
    )

    create_note(db, note)
    db.commit()
    db.refresh(note)

    assert note.id is not None
    assert note.title == "DFS"
    assert note.user_id == user.id


def test_get_note_by_id(db: Session, user: User):
    """
    Проверяет, что заметку можно найти по id.
    """
    category = Category(
        name="Graphs",
        user_id=user.id,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    note = Note(
        title="DFS",
        content="Test",
        category_id=category.id,
        user_id=user.id,
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    result = get_note_by_id(db, note.id)

    assert result is not None
    assert result.title == "DFS"


def test_get_all_notes(db: Session, user: User):
    """
    Проверяет, что можно получить все заметки.
    """
    category = Category(
        name="Graphs",
        user_id=user.id,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    db.add_all(
        [
            Note(
                title="DFS",
                content="Test1",
                category_id=category.id,
                user_id=user.id,
            ),
            Note(
                title="BFS",
                content="Test2",
                category_id=category.id,
                user_id=user.id,
            ),
        ]
    )
    db.commit()

    notes = get_all_notes(db)

    assert len(notes) == 2


def test_get_all_notes_by_user(db: Session, user: User):
    """
    Проверяет, что можно получить заметки конкретного пользователя.
    """
    category = Category(
        name="Graphs",
        user_id=user.id,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    db.add_all(
        [
            Note(
                title="DFS",
                content="Test1",
                category_id=category.id,
                user_id=user.id,
            ),
            Note(
                title="BFS",
                content="Test2",
                category_id=category.id,
                user_id=user.id,
            ),
        ]
    )
    db.commit()

    notes = get_all_notes_by_user(db, user.id)

    assert len(notes) == 2
    assert notes[0].user_id == user.id


def test_get_notes_by_category_id(db: Session, user: User):
    """
    Проверяет, что можно получить заметки по id категории.
    """
    category = Category(
        name="Graphs",
        user_id=user.id,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    db.add_all(
        [
            Note(
                title="DFS",
                content="Test1",
                category_id=category.id,
                user_id=user.id,
            ),
            Note(
                title="BFS",
                content="Test2",
                category_id=category.id,
                user_id=user.id,
            ),
        ]
    )
    db.commit()

    notes = get_notes_by_category_id(db, category.id)

    assert len(notes) == 2


def test_update_note(db: Session, user: User):
    """
    Проверяет, что заметку можно обновить.
    """
    category = Category(
        name="Graphs",
        user_id=user.id,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    note = Note(
        title="DFS",
        content="Test",
        category_id=category.id,
        user_id=user.id,
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    note.title = "BFS"
    note.content = "Updated Test"

    update_note(db, note)
    db.commit()
    db.refresh(note)

    assert note.title == "BFS"
    assert note.content == "Updated Test"


def test_delete_note(db: Session, user: User):
    """
    Проверяет, что заметку можно удалить.
    """
    category = Category(
        name="Graphs",
        user_id=user.id,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    note = Note(
        title="DFS",
        content="Test",
        category_id=category.id,
        user_id=user.id,
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    note_id = note.id

    delete_note(db, note)
    db.commit()

    assert get_note_by_id(db, note_id) is None
