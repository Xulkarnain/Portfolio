class AppException(Exception):
    """Base exception for application-level errors."""


class ResourceNotFoundException(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, resource_id: int | str):
        self.resource = resource
        self.resource_id = resource_id

        super().__init__(
            f"{resource} with id {resource_id} was not found"
        )

class DuplicateResourceException(AppException):
    """Raised when a resource with the same unique value already exists."""

    def __init__(self, resource: str, field: str, value: str):
        self.resource = resource
        self.field = field
        self.value = value

        super().__init__(
            f"{resource} with {field} '{value}' already exists"
        )


class InvalidReferenceException(AppException):
    """Raised when supplied related resource IDs are invalid."""

    def __init__(self, resource: str, invalid_ids: list[int]):
        self.resource = resource
        self.invalid_ids = invalid_ids

        super().__init__(
            f"Invalid {resource} IDs: {invalid_ids}"
        )


class PortfolioOwnerNotFoundException(AppException):
    """Raised when exactly one portfolio owner cannot be resolved."""

    def __init__(self):
        super().__init__(
            "A single portfolio owner must exist before creating projects"
        )

class InvalidInputException(AppException):
    """Raised when supplied input violates business rules."""

    def __init__(self, message: str):
        super().__init__(message)