from typing import Type

from core.di.repository import DIRepository
from core.enums.app.account.auth_provider import AuthProviderType
from core.enums.di.repository import RepositoryType, FilterFieldType
from application.base.service.base_service import BaseService
from core.enums.system.error_fields import ErrorFields
from core.messages.account.access_control import AccessControlMessages

from domain.account.entities.account_auth_profile import AccountAuthProfileEntity
from domain.account.entities.auth.provider_data import BaseAuthProviderData
from domain.account.repositories.account_auth_profile import AccountAuthProfileFilter, AccountAuthProfileRepository
from domain.base.exceptions import DomainValidationException
from domain.base.filters.equal_filter import EqualFilterField


class AccountAuthProfileService(
    BaseService[AccountAuthProfileEntity, AccountAuthProfileFilter, AccountAuthProfileRepository]):
    """
    Application-level service for working with AccountAuthProfileEntity.

    Responsibilities:
    - Resolve correct AccountAuthProfileRepository via DI
    - Provide CRUD and filtered_list operations (inherited from BaseService)
    - Add application-level validation and helper methods for auth profile logic
    """

    def __init__(self, repository_type: RepositoryType | None = None):
        super().__init__(AccountAuthProfileEntity, repository_type)
        self.eq: Type[EqualFilterField] = DIRepository.get_filter(FilterFieldType.EQUAL)

    @staticmethod
    async def ensure_is_valid_provider_data(
            provider_type: AuthProviderType, provider_data: BaseAuthProviderData
    ) -> None:
        if not provider_data.is_valid():
            raise DomainValidationException(AccessControlMessages.invalid_auth_provider_data(provider_type),
                                            field=ErrorFields.AUTH_PROVIDER_DATA)

    async def get_or_raise_by_provider_and_id(
            self, provider_type: AuthProviderType, provider_data: BaseAuthProviderData
    ) -> AccountAuthProfileEntity:
        auth_profile = await self.get_or_none_by_provider_and_id(provider_type, provider_data)
        if not auth_profile:
            raise DomainValidationException(AccessControlMessages.account_auth_profile_not_found(),
                                            field=ErrorFields.AUTH_PROVIDER_DATA)
        return auth_profile

    async def get_or_none_by_provider_and_id(
            self, provider_type: AuthProviderType, provider_data: BaseAuthProviderData
    ) -> AccountAuthProfileEntity | None:
        provider_id = str(provider_data.get_user_id())
        entities = await self.repository.filtered_list(
            AccountAuthProfileFilter(
                provider_id=self.eq(equal=provider_id),
                provider_type=self.eq(equal=provider_type)
            )
        )
        if len(entities) == 0:
            return None
        return entities[0]

    async def get_by_account_id(self, account_id: int) -> list[AccountAuthProfileEntity]:
        return await self.repository.filtered_list(
            AccountAuthProfileFilter(account_id=self.eq(equal=account_id))
        )
