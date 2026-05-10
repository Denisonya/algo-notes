import pytest

from app.schemas.note import NoteCreate
from app.services.note_service import (
    create_note_service,
    get_note_by_id_service,
)
from app.models import Category
from app.core.exceptions import NotFoundError


def test_create_note_service(db):
    category = Category(name="Graphs")
    db.add(category)
    db.commit()

    data = NoteCreate(
        title="DFS",
        content="Test",
        category_id=category.id
    )

    note = create_note_service(data, db)

    assert note.id is not None
    assert note.title == "DFS"


def test_get_note_not_found(db):
    with pytest.raises(NotFoundError):
        get_note_by_id_service(1000, db)
