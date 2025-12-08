from core.enums.system.logger.message_levels import LogMessageLevel
from core.exceptions.system import LoggerException
from core.helpers.func.date_time import get_local_time
from core.logger.base import LogMessage
from core.messages.system.no_localized_messages import SystemMessages


class Logger:

    @staticmethod
    def log(msg: LogMessage) -> None:
        """
        Accepts a structured log message and prints it.
        """
        data = msg.serialize()
        local_time, tz_name = get_local_time(msg.created_at)
        print(f"[{local_time.isoformat()} / {tz_name}] {data}")

    @classmethod
    def info(cls, msg: LogMessage) -> None:
        if msg.level.value != LogMessageLevel.INFO:
            raise LoggerException(SystemMessages.INVALID_LOG_LEVEL_INFO)
        cls.log(msg)

    @classmethod
    def warn(cls, msg: LogMessage) -> None:
        if msg.level.value != LogMessageLevel.WARN:
            raise LoggerException(SystemMessages.INVALID_LOG_LEVEL_WARN)
        cls.log(msg)

    @classmethod
    def error(cls, msg: LogMessage) -> None:
        if msg.level.value != LogMessageLevel.ERROR:
            raise LoggerException(SystemMessages.INVALID_LOG_LEVEL_ERROR)
        cls.log(msg)
