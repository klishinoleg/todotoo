from typing import Any

from application.base.dto.base import ItemDTO, ListDTO
from application.base.dto.geo import GeometryPointDTO, GeometryPolygonDTO
from core.enums.app.location.location_type import LocationType


class LocationDTO(ItemDTO):
    """
    Full representation of LocationEntity for external interfaces.
    Mirrors detailed location fields suitable for UI and map integrations.
    """
    name: str
    type: LocationType

    # Geometry
    point: GeometryPointDTO | None
    polygon: GeometryPolygonDTO | None

    # Address data
    address_raw: str | None
    address_structured: dict[str, Any] | None

    # Hierarchy
    parent_id: int | None

    # Images
    image: str | None
    image_small: str | None
    image_medium: str | None
    image_large: str | None
    is_active: bool


class LocationListDTO(ListDTO):
    """
    Lightweight version of LocationDTO for list views.
    Only fields required by listings are included.
    """
    name: str
    type: LocationType
    point: GeometryPointDTO | None
    parent_id: int | None
    is_active: bool
    image_small: str | None
