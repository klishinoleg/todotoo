from dataclasses import dataclass, field

from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin
from domain.base.mixins.with_active import WithActiveMixin
from domain.base.value_objects.geometry import GeometryPoint, GeometryPolygon
from domain.location.entities.location import LocationEntity


@dataclass(slots=True, kw_only=True)
class EventEntity(BaseEntity, WithActiveMixin, TimestampMixin):
    name: str
    description: str
    account_id: int
    point: GeometryPoint | None = None
    polygon: GeometryPolygon | None = None
    group_link: str | None = None
    image: str | None = None
    image_small: str | None = None
    image_medium: str | None = None
    image_large: str | None = None
    chat_link: str | None = None

    schedule_rule_ids: list[int] = field(default_factory=list)

    location_id: int | None = None
