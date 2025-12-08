from dataclasses import dataclass
from typing import Any

from core.enums.app.location.location_type import LocationType
from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin
from domain.base.mixins.with_active import WithActiveMixin
from domain.base.value_objects.geometry import GeometryPoint, GeometryPolygon


@dataclass(slots=True, kw_only=True)
class LocationEntity(BaseEntity, WithActiveMixin, TimestampMixin):
    """
    Represents a geographic location: point, area, place, or organization.
    Used for user events and future structured map data.
    """
    name: str
    type: LocationType
    point: GeometryPoint | None = None

    polygon: GeometryPolygon | None = None

    # Raw unformatted address from Google Geocoding
    address_raw: str | None = None

    # Structured address (country, city, street, house, etc.)
    address_structured: dict[str, Any] | None = None

    # For hierarchical locations (venue > floor > room)
    parent_id: int | None = None
    image: str | None = None
    image_small: str | None = None
    image_medium: str | None = None
    image_large: str | None = None
