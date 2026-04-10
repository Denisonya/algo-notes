class NotFoundError(Exception):
    """
    Entity is not found.
    """
    pass


class AlreadyExistsError(Exception):
    """
    Entity already exists.
    """
    pass
