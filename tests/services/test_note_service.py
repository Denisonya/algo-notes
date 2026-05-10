import pytest
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models import Category, Note, User
from app.schemas.category import CategoryCreate
from app.schemas.note import NoteCreate, NotePatch, NoteUpdate
from app.services.category_service import create_category_service
from app.services.note_service import (
    create_note_service,
    delete_note_service,
    get_all_notes_service,
    get_note_by_id_service,
    get_notes_by_category_id_service,
    patch_note_service,
    update_note_service,
)


def test_create_note_service(db: Session, user: User):
    """
    Проверяет, что сервис создает заметку для текущего пользователя.
    """
    category = create_category_service(
        CategoryCreate(name="Graphs"),
        db,
        user,
    )

    data = NoteCreate(
        title="DFS",
        content="Test",
        category_id=category.id,
    )

    note = create_note_service(data, db, user)

    assert note.id is not None
    assert note.title == "DFS"
    assert note.user_id == user.id
    assert note.category_id == category.id


def test_create_note_in_missing_category(db: Session, user: User):
    """
    Проверяет, что нельзя создать заметку в несуществующей категории.
    """
    data = NoteCreate(
        title="DFS",
        content="Test",
        category_id=1000,
    )

    with pytest.raises(NotFoundError):
        create_note_service(data, db, user)


def test_get_all_notes_service(db: Session, user: User):
    """
    Проверяет, что сервис возвращает все заметки текущего пользователя.
    """
    category = create_category_service(
        CategoryCreate(name="Graphs"),
        db,
        user,
    )

    create_note_service(
        NoteCreate(
            title="DFS",
            content="Test1",
            category_id=category.id,
        ),
        db,
        user,
    )

    create_note_service(
        NoteCreate(
            title="BFS",
            content="Test2",
            category_id=category.id,
        ),
        db,
        user,
    )

    notes = get_all_notes_service(db, user)

    assert len(notes) == 2


def test_get_note_by_id_service(db: Session, user: User):
    """
    Проверяет, что сервис возвращает заметку по id.
    """
    category = create_category_service(
        CategoryCreate(name="Graphs"),
        db,
        user,
    )

    note = create_note_service(
        NoteCreate(
            title="DFS",
            content="Test",
            category_id=category.id,
        ),
        db,
        user,
    )

    result = get_note_by_id_service(note.id, db, user)

    assert result.id == note.id
    assert result.title == "DFS"


def test_get_note_not_found(db: Session, user: User):
    """
    Проверяет, что для несуществующей заметки возникает NotFoundError.
    """
    with pytest.raises(NotFoundError):
        get_note_by_id_service(1000, db, user)


def test_get_notes_by_category_id_service(db: Session, user: User):
    """
    Проверяет, что сервис возвращает заметки по id категории.
    """
    category = create_category_service(
        CategoryCreate(name="Graphs"),
        db,
        user,
    )

    create_note_service(
        NoteCreate(
            title="DFS",
            content="Test1",
            category_id=category.id,
        ),
        db,
        user,
    )

    create_note_service(
        NoteCreate(
            title="BFS",
            content="Test2",
            category_id=category.id,
        ),
        db,
        user,
    )

    notes = get_notes_by_category_id_service(category.id, db, user)

    assert len(notes) == 2


def test_user_cannot_get_foreign_note(db: Session, user: User):
    """
    Проверяет, что пользователь не может получить чужую заметку.
    """
    another_user = User(
        username="alex",
        hashed_password="2000",
    )

    db.add(another_user)
    db.commit()
    db.refresh(another_user)

    foreign_category = Category(
        name="Foreign category",
        user_id=another_user.id,
    )

    db.add(foreign_category)
    db.commit()
    db.refresh(foreign_category)

    foreign_note = Note(
        title="Foreign note",
        content="Foreign content",
        category_id=foreign_category.id,
        user_id=another_user.id,
    )

    db.add(foreign_note)
    db.commit()
    db.refresh(foreign_note)

    with pytest.raises(NotFoundError):
        get_note_by_id_service(foreign_note.id, db, user)


def test_update_note(db: Session, user: User):
    """
    Проверяет, что сервис полностью обновляет заметку.
    """
    category = create_category_service(
        CategoryCreate(name="Graphs"),
        db,
        user,
    )

    note = create_note_service(
        NoteCreate(
            title="DFS",
            content="Test",
            category_id=category.id,
        ),
        db,
        user,
    )

    updated = update_note_service(
        note.id,
        NoteUpdate(
            title="BFS",
            content="Updated content",
            category_id=category.id,
        ),
        db,
        user,
    )

    assert updated.title == "BFS"
    assert updated.content == "Updated content"


def test_patch_note(db: Session, user: User):
    """
    Проверяет, что сервис частично обновляет заметку.
    """
    category = create_category_service(
        CategoryCreate(name="Graphs"),
        db,
        user,
    )

    note = create_note_service(
        NoteCreate(
            title="DFS",
            content="Test",
            category_id=category.id,
        ),
        db,
        user,
    )

    patched = patch_note_service(
        note.id,
        NotePatch(content="Patched content"),
        db,
        user,
    )

    assert patched.content == "Patched content"


def test_delete_note(db: Session, user: User):
    """
    Проверяет, что сервис удаляет заметку.
    """
    category = create_category_service(
        CategoryCreate(name="Graphs"),
        db,
        user,
    )

    note = create_note_service(
        NoteCreate(
            title="DFS",
            content="Test",
            category_id=category.id,
        ),
        db,
        user,
    )

    note_id = note.id

    delete_note_service(note_id, db, user)

    with pytest.raises(NotFoundError):
        get_note_by_id_service(note_id, db, user)
