from abc import ABC

from core.enums.app.account.auth_provider import AuthProviderType
from domain.account.entities.account_auth_profile import AccountAuthProfileEntity
from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.repository import BaseRepository


class AccountAuthProfileFilter[Q](BaseFilter[Q]):
    account_id: EqualFilterField[int, Q] | None = None
    provider_type: EqualFilterField[AuthProviderType, Q] | None = None
    provider_id: EqualFilterField[str, Q] | None = None


class AccountAuthProfileRepository[Q](
    BaseRepository[AccountAuthProfileEntity, AccountAuthProfileFilter[Q]], ABC
):
    ...
