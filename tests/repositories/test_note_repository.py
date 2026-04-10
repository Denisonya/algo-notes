from app.models import Note, Category
from app.repositories.note_repository import (
    create_note,
    get_note_by_id,
    get_notes_by_category_id,
)


def test_create_note(db):
    category = Category(name="Graphs")
    db.add(category)
    db.commit()

    note = Note(
        title="DFS",
        content="Test",
        category_id=category.id
    )

    create_note(db, note)
    db.commit()

    assert note.id is not None


def test_get_note_by_id(db):
    category = Category(name="Graphs")
    db.add(category)
    db.commit()

    note = Note(title="DFS", content="Test", category_id=category.id)
    db.add(note)
    db.commit()

    result = get_note_by_id(db, note.id)

    assert result is not None
    assert result.title == "DFS"


def test_get_notes_by_category_id(db):
    category = Category(name="Graphs")
    db.add(category)
    db.commit()

    db.add_all([
        Note(title="DFS", content="Test1", category_id=category.id),
        Note(title="BFS", content="Test2", category_id=category.id),
    ])
    db.commit()

    notes = get_notes_by_category_id(db, category.id)

    assert len(notes) == 2
