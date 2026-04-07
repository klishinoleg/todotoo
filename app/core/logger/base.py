from datetime import datetime

from pydantic import BaseModel, Field
from typing import Any, ClassVar

from core.enums.system.logger.message_levels import LogMessageLevel
from core.enums.system.logger.message_types import LogMessageType
from core.helpers.func.date_time import get_utc_time


class LogMessage(BaseModel):
    """
    Base class for all structured log messages.
    Each subclass MUST define:
        type: ClassVar[LogMessageType]
        level: ClassVar[LogMessageLevel]
    """
    created_at: datetime = Field(default_factory=get_utc_time)
    type: ClassVar[LogMessageType]
    level: ClassVar[LogMessageLevel]

    def serialize(self) -> dict:
        """
        Common JSON structure for every log record.
        """
        return {
            "type": self.type.value,
            "level": self.level.value,
            "payload": self.model_dump(),
        }


class AuthLogMessage(BaseModel):
    """
    Lightweight structured auth log record.
    Uses free-form `event` + `payload` for debugging auth flows.
    """

    created_at: datetime = Field(default_factory=get_utc_time)
    level: LogMessageLevel = LogMessageLevel.INFO
    event: str
    payload: dict[str, Any] = Field(default_factory=dict)

    def serialize(self) -> dict[str, Any]:
        return {
            "type": "auth",
            "level": self.level.value,
            "event": self.event,
            "payload": self.payload,
            "created_at": self.created_at.isoformat(),
        }
