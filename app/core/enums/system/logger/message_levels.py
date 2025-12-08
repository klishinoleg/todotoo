from enum import Enum


class LogMessageLevel(str, Enum):
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
