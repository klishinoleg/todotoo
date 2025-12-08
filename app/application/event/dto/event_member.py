from application.base.dto.base import ItemDTO, ListDTO


class EventMemberDTO(ItemDTO):
    """
    Full representation of EventMemberEntity for external interfaces.
    Mirrors detailed membership fields suitable for UI and integrations.
    """
    event_occurrence_id: int
    event_id: int
    account_id: int
    has_accepted: bool


class EventMemberListDTO(ListDTO):
    """
    Lightweight version of EventMemberDTO for list views.
    Only fields required by listings are included.
    """
    event_id: int
    account_id: int
    has_accepted: bool
