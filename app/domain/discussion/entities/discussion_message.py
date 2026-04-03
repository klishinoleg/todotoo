from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class DiscussionMessageEntity(BaseEntity, TimestampMixin):
    discussion_id: int
    account_id: int
    text: str

