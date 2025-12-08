from abc import ABC
from datetime import datetime

from domain.account.entities.account_session import AccountSessionEntity
from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.range_filter import RangeFilterField
from domain.base.repository import BaseRepository


class AccountSessionFilter[Q](BaseFilter[Q]):
    """
    Domain filter for account sessions.

    Allows filtering by:
        - started_at:   datetime range
        - closed_at:    datetime range
        - account_id:   integer range
        - requests:     integer range
    """

    started_at: RangeFilterField[datetime, Q] | None = None
    closed_at: RangeFilterField[datetime, Q] | None = None
    account_id: EqualFilterField[int, Q] | None = None
    requests: RangeFilterField[int, Q] | None = None


class AccountSessionRepository[Q](BaseRepository[AccountSessionEntity, AccountSessionFilter[Q]], ABC):
    """Abstract repository interface for account session storage."""
    ...
