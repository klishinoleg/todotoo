from core.enums.di.repository import RepositoryType
from application.base.service.base_service import BaseService

from domain.account.entities.account_auth_profile import AccountAuthProfileEntity
from domain.account.repositories.account_auth_profile import AccountAuthProfileFilter


class AccountAuthProfileService(BaseService[AccountAuthProfileEntity, AccountAuthProfileFilter]):
    """
    Application-level service for working with AccountAuthProfileEntity.

    Responsibilities:
    - Resolve correct AccountAuthProfileRepository via DI
    - Provide CRUD and filtered_list operations (inherited from BaseService)
    - Add application-level validation and helper methods for auth profile logic
    """

    def __init__(self, repository_type: RepositoryType | None = None):
        super().__init__(AccountAuthProfileEntity, repository_type)
