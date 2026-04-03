# app/core/messages/system/no_localized_messages.py

class SystemMessages:
    """
    Central storage for system-level non-localized messages.
    These strings are not intended for UI and must not be translated.
    """

    # Logger
    INVALID_LOG_LEVEL_INFO = "Invalid log level for info()"
    INVALID_LOG_LEVEL_WARN = "Invalid log level for warn()"
    INVALID_LOG_LEVEL_ERROR = "Invalid log level for error()"
    INVALID_LOG_MESSAGE_TYPE = "Invalid log message type"
    INVALID_LOG_MESSAGE_CLASS = "Provided object is not a valid LogMessage subclass"
    UNKNOWN_LOGGER_ERROR = "Unknown logger exception occurred"

    # Geometry: generic
    UNKNOWN_GEOMETRY_ERROR = "Unknown geometry exception occurred"
    UNKNOWN_GEOMETRY_TYPE = "Unknown geometry type"
    INVALID_GEOMETRY_DATA = "Invalid geometry data"
    INVALID_GEOMETRY_TYPE = "Invalid geometry type"

    # Geometry: specific invalid formats
    INVALID_GEOMETRY_POINT = "Invalid geometry Point format"
    INVALID_GEOMETRY_CIRCLE = "Invalid geometry Circle format"
    INVALID_GEOMETRY_POLYGON = "Invalid geometry Polygon format"

    # Repository: specific repositories exceptions
    UNKNOW_REPOSITORY_ERROR = "Unknown repository exception occurred"
    UNKNOWN_REPOSITORY_TYPE = "Repository type is not registered or not supported"
    REPOSITORY_NOT_REGISTERED = "Repository implementation is not registered"
    REPOSITORY_TRANSACTION_MANAGER_NOT_REGISTERED = "Repository transaction manager is not registered"
    FILTER_NOT_REGISTERED = "Filter implementation is not registered"
    STORAGE_PROVIDER_NOT_REGISTERED = "Storage provider implementation is not registered"

    # Auth provider: specific auth provider exceptions
    UNKNOW_AUTH_PROVIDER_ERROR = "Unknown auth provider exception occurred"
    AUTH_PROVIDER_NOT_REGISTERED = "Auth provider implementation is not registered"

    # Access control
    UNKNOWN_ACCESS_CONTROL_ERROR = "Unknown access control exception occurred"
    ACCESS_CONTROL_PROVIDER_NOT_REGISTERED = "Access control provider implementation is not registered"
    PASSWORD_HASHER_NOT_REGISTERED = "Password hasher implementation is not registered"
    AUTH_PROFILE_NOT_FOUND = "Auth profile not found"
    INVALID_PASSWORD = "Invalid password"
    INVALID_ACCESS_TOKEN = "Invalid access token"
    ACCESS_TOKEN_EXPIRED = "Access token expired"
    NOT_AUTHORIZED = "Not authorized"
    NOT_ENOUGH_PERMISSIONS = "Not enough permissions"
