from core.enums.di.repository import RepositoryType
from application.base.service.base_service import BaseService

from domain.account.entities.account_session import AccountSessionEntity
from domain.account.repositories.account_session import AccountSessionRepository, AccountSessionFilter


class AccountSessionService(BaseService[AccountSessionEntity, AccountSessionFilter]):
    """
    Application-level service for working with AccountSessionEntity.

    Responsibilities:
    - Resolve correct AccountSessionRepository via DI
    - Provide CRUD and filtered_list operations (inherited from BaseService)
    - Add application-level validation and helper methods for session logic
    """

    def __init__(self, repository_type: RepositoryType | None = None):
        super().__init__(AccountSessionEntity, repository_type)
