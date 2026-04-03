from dataclasses import dataclass

from core.enums.app.motivation.motivator_type import MotivatorTypeEnum
from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class MotivatorEntity(BaseEntity, TimestampMixin):
    idea_id: int
    type: MotivatorTypeEnum
    title: str | None = None
    description: str | None = None
    image_url: str | None = None
    video_url: str | None = None
    external_url: str | None = None
    created_by: int

