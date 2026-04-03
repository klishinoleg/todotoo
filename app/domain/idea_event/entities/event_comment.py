from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class IdeaEventCommentEntity(BaseEntity, TimestampMixin):
    event_id: int
    account_id: int
    text: str

