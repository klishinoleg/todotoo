from typing import ClassVar

from core.enums.system.logger.message_levels import LogMessageLevel
from core.enums.system.logger.message_types import LogMessageType
from core.logger.base import LogMessage


class MeasureFuncTimeMessage(LogMessage):
    type: ClassVar[LogMessageType] = LogMessageType.MEASURE_FUNC_TIME
    level: ClassVar[LogMessageLevel] = LogMessageLevel.INFO

    name: str
    time: float
