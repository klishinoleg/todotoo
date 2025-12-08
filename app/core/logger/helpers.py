from core.enums.system.logger.message_types import LogMessageType
from core.logger.base import LogMessage
from core.logger.registry import LOG_MESSAGE_MAP, LOG_MESSAGE_TYPE_FIELD, LOG_MESSAGE_PAYLOAD_FIELD


def parse_log_record(record: dict) -> LogMessage:
    msg_type = LogMessageType(record[LOG_MESSAGE_TYPE_FIELD])
    cls = LOG_MESSAGE_MAP[msg_type]
    return cls(**record[LOG_MESSAGE_PAYLOAD_FIELD])
