from abc import ABC

from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.bool_filter import BoolFilterField
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.string_filters import StringEqualFilterField
from domain.base.repository import BaseRepository
from domain.tag.entities.tag import TagEntity


class TagFilter[Q](BaseFilter[Q]):
    name: StringEqualFilterField[Q] | None = None
    slug: StringEqualFilterField[Q] | None = None
    parent_id: EqualFilterField[int, Q] | None = None
    is_active: BoolFilterField[Q] | None = None


class TagRepository[Q](BaseRepository[TagEntity, TagFilter[Q]], ABC):
    ...
