from application.base.dto.base import ItemDTO, ListDTO


class EventOccurrenceMessageDTO(ItemDTO):
    """
    Full representation of EventOccurrenceMessageEntity for external interfaces.
    Mirrors detailed message fields suitable for UI and integrations.
    """
    event_occurrence_id: int
    parent_message_id: int | None
    event_id: int
    event_member_id: int | None

    text: str
    image: str | None

    # From WithActiveMixin / TimestampMixin if needed by API
    is_active: bool
    # created_at: datetime
    # updated_at: datetime | None


class EventOccurrenceMessageListDTO(ListDTO):
    """
    Lightweight version of EventOccurrenceMessageDTO for list views.
    Only fields required by listings are included.
    """
    event_occurrence_id: int
    event_id: int
    event_member_id: int | None
    text: str
    image: str | None
    is_active: bool
