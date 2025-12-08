from typing import ClassVar

from core.enums.system.logger.message_levels import LogMessageLevel
from core.enums.system.logger.message_types import LogMessageType
from core.logger.base import LogMessage


class ObjCreatedMessage(LogMessage):
    type: ClassVar[LogMessageType] = LogMessageType.OBJ_CREATED
    level: ClassVar[LogMessageLevel] = LogMessageLevel.INFO

    account_id: int | None = None
    object_type: str
    object_id: int
