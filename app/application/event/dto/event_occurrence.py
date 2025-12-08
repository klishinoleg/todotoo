from datetime import datetime

from application.base.dto.base import ItemDTO, ListDTO


class EventOccurrenceDTO(ItemDTO):
    """
    Full representation of EventOccurrenceEntity for external interfaces.
    Mirrors detailed occurrence fields suitable for UI and integrations.
    """
    event_id: int
    start_at: datetime
    end_at: datetime
    members_count: int
    location_id: int | None
    is_canceled: bool
    is_finished: bool


class EventOccurrenceListDTO(ListDTO):
    """
    Lightweight version of EventOccurrenceDTO for list views.
    Only fields required by listings are included.
    """
    event_id: int
    start_at: datetime
    end_at: datetime
    is_canceled: bool
    is_finished: bool
