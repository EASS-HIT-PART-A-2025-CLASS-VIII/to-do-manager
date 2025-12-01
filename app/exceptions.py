class TaskNotFoundError(Exception):
    """Raised when a task with the given ID does not exist."""
    pass


class RepositoryError(Exception):
    """Raised for general repository-level errors."""
    pass