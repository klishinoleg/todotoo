from typing import ClassVar

from core.enums.system.logger.message_levels import LogMessageLevel
from core.enums.system.logger.message_types import LogMessageType
from core.logger.base import LogMessage


class NotFoundMessage(LogMessage):
    type: ClassVar[LogMessageType] = LogMessageType.NOT_FOUND
    level: ClassVar[LogMessageLevel] = LogMessageLevel.ERROR

    field_name: str
    field_value: str | int
