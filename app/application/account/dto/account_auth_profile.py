from datetime import datetime

from application.base.dto.base import ListDTO, ItemDTO
from core.enums.app.account.auth_provider import AuthProviderType


class AccountAuthProfileDTO(ItemDTO):
    """
    Full representation of AccountAuthProfile entity for external interfaces.
    Mirrors detailed entity fields suitable for UI and integrations.
    """
    account_id: int
    provider: AuthProviderType
    provider_account_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime | None
    last_login_at: datetime | None


class AccountAuthProfileListDTO(ListDTO):
    """
    Lightweight version of AccountAuthProfileDTO for list views.
    Only fields required by listings are included.
    """
    provider: AuthProviderType
    is_active: bool
