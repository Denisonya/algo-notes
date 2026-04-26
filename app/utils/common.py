def apply_updates(instance: object, data: dict) -> None:
    """
    Apply partial updates to SQLAlchemy model instance.

    :param instance: SQLAlchemy model instance
    :param data: dict with fields to update
    """
    for field, value in data.items():
        if hasattr(instance, field):
            setattr(instance, field, value)
