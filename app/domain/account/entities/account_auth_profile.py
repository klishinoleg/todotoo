from dataclasses import dataclass

from core.enums.app.account.auth_provider import AuthProviderType
from domain.account.entities.auth.provider_data import BaseProviderData
from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class AccountAuthProfileEntity[PD: BaseProviderData](BaseEntity, TimestampMixin):
    account_id: int
    provider_type: AuthProviderType
    provider_id: str
    provider_data: PD
    language_code: str | None
