from datetime import datetime

from application.base.dto.base import ItemDTO, ListDTO
from application.base.dto.geo import GeometryPointDTO, GeometryPolygonDTO


class EventDTO(ItemDTO):
    """
    Full representation of EventEntity for external interfaces.
    Mirrors detailed event fields suitable for UI and integrations.
    """
    name: str
    description: str
    account_id: int

    # Geometry
    point: GeometryPointDTO | None
    polygon: GeometryPolygonDTO | None

    # Links & media
    group_link: str | None
    chat_link: str | None
    image: str | None
    image_small: str | None
    image_medium: str | None
    image_large: str | None

    # Schedule rules (store IDs for separate loading/expansion)
    schedule_rule_ids: list[int]

    # Linked location
    location_id: int | None

    # State
    is_active: bool

    created_at: datetime
    updated_at: datetime | None


class EventListDTO(ListDTO):
    """
    Lightweight version of EventDTO for list views.
    Only fields required by listings are included.
    """
    name: str
    description: str | None
    image_small: str | None
    account_id: int
