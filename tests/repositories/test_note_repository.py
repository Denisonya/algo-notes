from app.repositories import note_repository, category_repository


def test_create_note(db):
    category = category_repository.create(db, "Work")

    note_data = {
        "title": "Test",
        "content": "Hello",
        "category_id": category.id
    }

    note = note_repository.create(db, note_data)

    assert note.id is not None
    assert note.title == "Test"


def test_get_all_notes(db):
    category = category_repository.create(db, "Work")

    note_repository.create(db, {
        "title": "Test1",
        "content": "Hello",
        "category_id": category.id
    })

    notes = note_repository.get_all(db)

    assert len(notes) == 1


def test_filter_notes_by_category(db):
    cat1 = category_repository.create(db, "Work")
    cat2 = category_repository.create(db, "Personal")

    note_repository.create(db, {
        "title": "Work note",
        "content": "Hello",
        "category_id": cat1.id
    })

    note_repository.create(db, {
        "title": "Personal note",
        "content": "Hi",
        "category_id": cat2.id
    })

    notes = note_repository.get_all(db)

    assert len(notes) == 1
    assert notes[0].title == "Work note"


def test_get_note_by_id(db):
    category = category_repository.create(db, "Work")

    note = note_repository.create(db, {
        "title": "Test",
        "content": "Hello",
        "category_id": category.id
    })

    found = note_repository.get_by_id(db, note.id)

    assert found is not None
    assert found.id == note.id
