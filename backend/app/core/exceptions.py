class AppException(Exception):
    """Base exception for application-level errors."""


class ResourceNotFoundException(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, resource_id: int):
        self.resource = resource
        self.resource_id = resource_id

        super().__init__(
            f"{resource} with id {resource_id} was not found"
        )