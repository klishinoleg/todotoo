from core.enums.di.repository import RepositoryType
from application.base.service.base_service import BaseService
from core.enums.system.error_fields import ErrorFields
from core.messages.account.access_control import AccessControlMessages

from domain.account.entities.account import AccountEntity
from domain.account.repositories.account import AccountFilter, AccountRepository
from domain.base.exceptions import DomainValidationException


class AccountService(BaseService[AccountEntity, AccountFilter, AccountRepository]):
    """
    Application-level service for working with AccountEntity.

    Responsibilities:
    - Resolve correct AccountRepository via DI
    - Provide CRUD and filtered_list operations (inherited from BaseService)
    - Add application-level validation and helper methods for account logic
    """

    def __init__(self, repository_type: RepositoryType | None = None):
        super().__init__(AccountEntity, repository_type)

    async def get_or_raise_validation(self, account_id: int) -> AccountEntity:
        account = await self.get(account_id)
        if not account:
            raise DomainValidationException(
                message=AccessControlMessages.account_not_found(),
                field=ErrorFields.ACCOUNT
            )
        return account
