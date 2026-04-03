from abc import ABC

from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.string_filters import TextFilterField
from domain.base.repository import BaseRepository
from domain.plan.entities.plan import PlanEntity
from domain.plan.entities.plan_step import PlanStepEntity


class PlanFilter[Q](BaseFilter[Q]):
    idea_id: EqualFilterField[int, Q] | None = None
    title: TextFilterField[Q] | None = None
    created_by: EqualFilterField[int, Q] | None = None


class PlanRepository[Q](BaseRepository[PlanEntity, PlanFilter[Q]], ABC):
    ...


class PlanStepFilter[Q](BaseFilter[Q]):
    plan_id: EqualFilterField[int, Q] | None = None
    assigned_to: EqualFilterField[int, Q] | None = None
    status: EqualFilterField[str, Q] | None = None
    title: TextFilterField[Q] | None = None


class PlanStepRepository[Q](BaseRepository[PlanStepEntity, PlanStepFilter[Q]], ABC):
    ...

