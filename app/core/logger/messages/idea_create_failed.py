from typing import Any, ClassVar

from core.enums.system.logger.message_levels import LogMessageLevel
from core.enums.system.logger.message_types import LogMessageType
from core.logger.base import LogMessage


class IdeaCreateFailedMessage(LogMessage):
    type: ClassVar[LogMessageType] = LogMessageType.IDEA_CREATE_FAILED
    level: ClassVar[LogMessageLevel] = LogMessageLevel.WARN

    authorized: bool
    account_id: int | None = None
    reason: str
    payload: dict[str, Any]
