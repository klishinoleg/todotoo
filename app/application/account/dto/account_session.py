from datetime import datetime

from application.base.dto.base import ItemDTO, ListDTO


class AccountSessionDTO(ItemDTO):
    """
    Full representation of AccountSessionEntity for external interfaces.
    Mirrors detailed session fields suitable for UI and analytics.
    """
    account_id: int
    requests: int
    started_at: datetime
    closed_at: datetime | None


class AccountSessionListDTO(ListDTO):
    """
    Lightweight version of AccountSessionDTO for list views.
    Only fields required by listings are included.
    """
    account_id: int
    started_at: datetime
    closed_at: datetime | None
    requests: int
