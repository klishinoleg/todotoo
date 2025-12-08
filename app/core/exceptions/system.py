# app/core/exceptions/system.py

from core.exceptions.base import BaseAppException
from core.messages.system.no_localized_messages import SystemMessages


class LoggerException(BaseAppException):
    """
    Exception related to logging subsystem.
    Examples:
        - Incorrect log level
        - Invalid message object
        - Registry mapping error
    """

    def __init__(self, message: str = SystemMessages.UNKNOWN_LOGGER_ERROR):
        super().__init__(message)


class GeometryException(BaseAppException):
    """
    Represents an exception specific to geometry-related errors.

    This class is a specialized exception designed to handle and represent errors
    or issues that arise within geometry-related operations or computations. It
    inherits from the base application exception and can be utilized for error
    handling specifically in geometrical contexts.
    """

    def __init__(self, message: str = SystemMessages.UNKNOWN_LOGGER_ERROR):
        super().__init__(message)


class RepositoryException(BaseAppException):
    """
    Represents an exception that occurs in repository operations.

    This class is intended to handle and represent errors specifically related
    to the repository layer. It inherits from the base application exception
    class to provide additional context or customization for repository-related
    exceptions.
    """

    def __init__(self, message: str = SystemMessages.UNKNOW_REPOSITORY_ERROR):
        super().__init__(message)


class AuthProviderException(BaseAppException):
    """
    Exception raised for errors related to authentication providers.

    This exception serves as a base exception for any issues arising
    from the usage or interaction with authentication providers in the application.
    """

    def __init__(self, message: str = SystemMessages.UNKNOW_AUTH_PROVIDER_ERROR):
        super().__init__(message)
