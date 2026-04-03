from abc import ABC

from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.bool_filter import BoolFilterField
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.string_filters import TextFilterField
from domain.base.repository import BaseRepository
from domain.idea.entities.idea import IdeaEntity


class IdeaFilter[Q](BaseFilter[Q]):
    creator_id: EqualFilterField[int, Q] | None = None
    visibility: EqualFilterField[str, Q] | None = None
    status: EqualFilterField[str, Q] | None = None
    is_active: BoolFilterField[Q] | None = None
    title: TextFilterField[Q] | None = None


class IdeaRepository[Q](BaseRepository[IdeaEntity, IdeaFilter[Q]], ABC):
    ...

