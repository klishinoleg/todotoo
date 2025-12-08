from typing import Union

from core.logger.base import LogMessage
from core.logger.messages.already_exist import AlreadyExistMessage
from core.logger.messages.not_found import NotFoundMessage
from core.logger.messages.obj_created import ObjCreatedMessage
from core.logger.messages.obj_deleted import ObjDeletedMessage
from core.logger.messages.obj_updated import ObjUpdatedMessage

AllLogMessages = Union[
    AlreadyExistMessage,
    NotFoundMessage,
    ObjCreatedMessage,
    ObjDeletedMessage,
    ObjUpdatedMessage,
]

LOG_MESSAGE_TYPE_FIELD = "type"
LOG_MESSAGE_PAYLOAD_FIELD = "payload"

# Dict to restore by type
LOG_MESSAGE_CLASSES: list[type[LogMessage]] = [
    AlreadyExistMessage,
    NotFoundMessage,
    ObjCreatedMessage,
    ObjDeletedMessage,
    ObjUpdatedMessage,
]

LOG_MESSAGE_MAP: dict[str, type[LogMessage]] = {
    cls.type: cls
    for cls in LOG_MESSAGE_CLASSES
}
