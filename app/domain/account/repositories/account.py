from abc import ABC
from datetime import datetime

from core.enums.app.account.gender import Gender
from domain.account.entities.account import AccountEntity
from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.bool_filter import BoolFilterField
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.range_filter import RangeFilterField
from domain.base.repository import BaseRepository


class AccountFilter[Q](BaseFilter[Q]):
    username: EqualFilterField[str, Q] | None = None
    email: EqualFilterField[str, Q] | None = None
    language: EqualFilterField[str, Q] | None = None
    gender: EqualFilterField[Gender, Q] | None = None
    create_at: RangeFilterField[datetime, Q] | None = None
    is_active: BoolFilterField[Q] | None = None


class AccountRepository[Q](BaseRepository[AccountEntity, AccountFilter[Q]], ABC):
    ...
