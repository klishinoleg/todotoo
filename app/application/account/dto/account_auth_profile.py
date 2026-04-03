from datetime import datetime

from application.base.dto.base import ListDTO, ItemDTO
from core.enums.app.account.auth_provider import AuthProviderType


class AccountAuthProfileDTO(ItemDTO):
    """
    Full representation of AccountAuthProfile entity for external interfaces.
    Mirrors detailed entity fields suitable for UI and integrations.
    """
    account_id: int
    provider_type: AuthProviderType
    provider_id: str
    language_code: str | None
    created_at: datetime
    updated_at: datetime | None


class AccountAuthProfileListDTO(ListDTO):
    """
    Lightweight version of AccountAuthProfileDTO for list views.
    Only fields required by listings are included.
    """
    provider_type: AuthProviderType
    provider_id: str
