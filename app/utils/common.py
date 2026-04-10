def apply_updates(instance, data: dict):
    """
    Apply partial updates to SQLAlchemy model instance.

    :param instance: SQLAlchemy model instance
    :param data: dict with fields to update
    """
    for field, value in data.items():
        if value is not None and hasattr(instance, field):
            setattr(instance, field, value)
