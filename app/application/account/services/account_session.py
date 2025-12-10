from typing import Type

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType, FilterFieldType
from application.base.service.base_service import BaseService

from domain.account.entities.account_session import AccountSessionEntity
from domain.account.repositories.account_session import AccountSessionRepository, AccountSessionFilter
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.range_filter import RangeFilterField


class AccountSessionService(BaseService[AccountSessionEntity, AccountSessionFilter, AccountSessionRepository]):
    """
    Application-level service for working with AccountSessionEntity.

    Responsibilities:
    - Resolve correct AccountSessionRepository via DI
    - Provide CRUD and filtered_list operations (inherited from BaseService)
    - Add application-level validation and helper methods for session logic
    """

    def __init__(self, repository_type: RepositoryType | None = None):
        super().__init__(AccountSessionEntity, repository_type)
        self.eq: Type[EqualFilterField] = DIRepository.get_filter(FilterFieldType.EQUAL)
        self.range: Type[RangeFilterField] = DIRepository.get_filter(FilterFieldType.RANGE)

    async def get_or_create_active(self, account_id: int) -> AccountSessionEntity:
        active_sessions = await self.repository.filtered_list(
            AccountSessionFilter(
                closed_at=self.range(is_null=True),
                account_id=self.eq(equal=account_id)
            )
        )
        if len(active_sessions) == 0:
            new_session = AccountSessionEntity.create_from_account_id(account_id)
            active_session = await self.create(new_session)
        else:
            active_session = active_sessions[0]
        assert active_session is not None
        return active_session
