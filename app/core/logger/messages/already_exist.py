from typing import ClassVar

from core.enums.system.logger.message_levels import LogMessageLevel
from core.enums.system.logger.message_types import LogMessageType
from core.logger.base import LogMessage


class AlreadyExistMessage(LogMessage):
    type: ClassVar[LogMessageType] = LogMessageType.ALREADY_EXIST
    level: ClassVar[LogMessageLevel] = LogMessageLevel.WARN

    model: str
    id: str
