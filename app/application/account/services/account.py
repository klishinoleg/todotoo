from core.enums.di.repository import RepositoryType
from application.base.service.base_service import BaseService

from domain.account.entities.account import AccountEntity
from domain.account.repositories.account import AccountFilter


class AccountService(BaseService[AccountEntity, AccountFilter]):
    """
    Application-level service for working with AccountEntity.

    Responsibilities:
    - Resolve correct AccountRepository via DI
    - Provide CRUD and filtered_list operations (inherited from BaseService)
    - Add application-level validation and helper methods for account logic
    """

    def __init__(self, repository_type: RepositoryType | None = None):
        super().__init__(AccountEntity, repository_type)
