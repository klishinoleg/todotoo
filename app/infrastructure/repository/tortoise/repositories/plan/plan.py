from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.plan.entities.plan import PlanEntity
from domain.plan.repositories.plan import PlanFilter, PlanRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.plan.plan import PlanModel


class PlanTortoiseRepository(
    PlanRepository[QuerySet],
    BaseTortoiseRepository[PlanEntity, PlanFilter[QuerySet], PlanModel],
):
    model: Type[PlanModel] = PlanModel
    entity_cls: Type[PlanEntity] = PlanEntity

    async def to_entity(self, model: PlanModel) -> PlanEntity:
        return PlanEntity(
            id=model.id,
            idea_id=model.idea_id,
            title=model.title,
            description=model.description,
            icon=model.icon,
            position=model.position,
            created_by=model.created_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: PlanEntity) -> PlanModel:
        payload: dict[str, object] = {
            "idea_id": entity.idea_id,
            "title": entity.title,
            "description": entity.description,
            "icon": entity.icon,
            "position": entity.position,
            "created_by": entity.created_by,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(PlanEntity, PlanTortoiseRepository, RepositoryType.TORTOISE)

