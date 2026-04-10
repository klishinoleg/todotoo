from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from core.enums.app.plan.plan_step_status import PlanStepStatusEnum
from domain.plan.entities.plan_step import PlanStepEntity
from domain.plan.repositories.plan import PlanStepFilter, PlanStepRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.plan.plan_step import PlanStepModel


class PlanStepTortoiseRepository(
    PlanStepRepository[QuerySet],
    BaseTortoiseRepository[PlanStepEntity, PlanStepFilter[QuerySet], PlanStepModel],
):
    model: Type[PlanStepModel] = PlanStepModel
    entity_cls: Type[PlanStepEntity] = PlanStepEntity

    async def to_entity(self, model: PlanStepModel) -> PlanStepEntity:
        return PlanStepEntity(
            id=model.id,
            plan_id=model.plan_id,
            title=model.title,
            description=model.description,
            icon=model.icon,
            position=model.position,
            status=PlanStepStatusEnum(model.status),
            assigned_to=model.assigned_to,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: PlanStepEntity) -> PlanStepModel:
        payload: dict[str, object] = {
            "plan_id": entity.plan_id,
            "title": entity.title,
            "description": entity.description,
            "icon": entity.icon,
            "position": entity.position,
            "status": str(entity.status),
            "assigned_to": entity.assigned_to,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(PlanStepEntity, PlanStepTortoiseRepository, RepositoryType.TORTOISE)

