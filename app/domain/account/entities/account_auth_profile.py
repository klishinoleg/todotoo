from dataclasses import dataclass

from core.enums.app.account.auth_provider import AuthProviderType
from domain.account.entities.auth.provider_data import BaseAuthProviderData
from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class AccountAuthProfileEntity[PD: BaseAuthProviderData](BaseEntity, TimestampMixin):
    account_id: int
    provider_type: AuthProviderType
    provider_id: str
    provider_data: PD
    language_code: str | None

    @classmethod
    def create_from_provider_type_and_data(
            cls,
            provider_type: AuthProviderType,
            account_id: int,
            provider_data: PD) -> "AccountAuthProfileEntity":
        return cls(account_id=account_id, provider_type=provider_type,
                   provider_id=str(provider_data.get_user_id()),
                   language_code=provider_data.get_language_code(), provider_data=provider_data)
