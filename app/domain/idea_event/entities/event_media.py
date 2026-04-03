from dataclasses import dataclass

from core.enums.app.idea_event.media_type import MediaTypeEnum
from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class IdeaEventMediaEntity(BaseEntity, TimestampMixin):
    event_id: int
    type: MediaTypeEnum
    url: str
    preview_url: str | None = None
    created_by: int

