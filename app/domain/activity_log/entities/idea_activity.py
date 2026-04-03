from dataclasses import dataclass, field
from typing import Any

from core.enums.app.activity_log.idea_activity_type import IdeaActivityTypeEnum
from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class IdeaActivityEntity(BaseEntity, TimestampMixin):
    idea_id: int
    account_id: int | None = None
    type: IdeaActivityTypeEnum
    payload: dict[str, Any] = field(default_factory=dict)

