class BaseAppException(Exception):
    """
    Base class for all application-level exceptions.

    - Contains no business logic.
    - Designed to be extended by domain / system exceptions.
    """
    pass
