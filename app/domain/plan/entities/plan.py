from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class PlanEntity(BaseEntity, TimestampMixin):
    idea_id: int
    title: str
    description: str | None = None
    icon: str | None = None
    position: int = 0
    created_by: int

