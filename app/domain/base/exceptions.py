from core.enums.system.error_fields import ErrorFields
from core.exceptions.base import BaseAppException


class DomainException(BaseAppException):
    """
    Base exception for all domain-level errors.

    All exceptions inside the domain layer should inherit from this class.
    """
    ...


class DomainValidationException(BaseAppException):
    """
    Thrown when domain validation rules are violated.

    Used when entity state or input data does not satisfy business logic.
    """

    def __init__(
            self,
            message: str,
            *args: tuple,
            field: ErrorFields = ErrorFields.DETAILS
    ) -> None:
        self.message: str = message
        self.field: ErrorFields = field
        super().__init__(self.message, *args)

    def __repr__(self) -> str:
        return self.message

    def __str__(self) -> str:
        return self.message


class EntityException(DomainException):
    """
    Base exception for all entity-related domain errors.
    """
    ...


class EntityNotFound(EntityException):
    """
    Raised when an entity cannot be found in repository.
    """
    ...


class EntityPermissionDenied(EntityException):
    """
    Raised when access to an entity is denied.

    Default error used when Accessor has no specific validator
    or validator returns False.
    """
    ...
