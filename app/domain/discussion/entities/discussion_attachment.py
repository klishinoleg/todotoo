from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class DiscussionAttachmentEntity(BaseEntity, TimestampMixin):
    message_id: int
    file_url: str
    file_type: str

