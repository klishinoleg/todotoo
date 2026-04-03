from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class DiscussionEntity(BaseEntity, TimestampMixin):
    idea_id: int
    title: str
    created_by: int

