from abc import ABC

from domain.activity_log.entities.idea_activity import IdeaActivityEntity
from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.repository import BaseRepository


class IdeaActivityFilter[Q](BaseFilter[Q]):
    idea_id: EqualFilterField[int, Q] | None = None
    account_id: EqualFilterField[int, Q] | None = None
    type: EqualFilterField[str, Q] | None = None


class IdeaActivityRepository[Q](BaseRepository[IdeaActivityEntity, IdeaActivityFilter[Q]], ABC):
    ...

