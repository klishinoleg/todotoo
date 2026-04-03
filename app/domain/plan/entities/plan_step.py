from dataclasses import dataclass

from core.enums.app.plan.plan_step_status import PlanStepStatusEnum
from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class PlanStepEntity(BaseEntity, TimestampMixin):
    plan_id: int
    title: str
    description: str | None = None
    icon: str | None = None
    position: int = 0
    status: PlanStepStatusEnum = PlanStepStatusEnum.TODO
    assigned_to: int | None = None

