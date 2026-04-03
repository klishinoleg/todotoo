from abc import ABC

from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.string_filters import TextFilterField
from domain.base.repository import BaseRepository
from domain.motivation.entities.motivator import MotivatorEntity


class MotivatorFilter[Q](BaseFilter[Q]):
    idea_id: EqualFilterField[int, Q] | None = None
    created_by: EqualFilterField[int, Q] | None = None
    type: EqualFilterField[str, Q] | None = None
    title: TextFilterField[Q] | None = None


class MotivatorRepository[Q](BaseRepository[MotivatorEntity, MotivatorFilter[Q]], ABC):
    ...

