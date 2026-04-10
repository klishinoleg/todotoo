from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from core.enums.app.motivation.motivator_type import MotivatorTypeEnum
from domain.motivation.entities.motivator import MotivatorEntity
from domain.motivation.repositories.motivator import MotivatorFilter, MotivatorRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.motivation.motivator import MotivatorModel


class MotivatorTortoiseRepository(
    MotivatorRepository[QuerySet],
    BaseTortoiseRepository[MotivatorEntity, MotivatorFilter[QuerySet], MotivatorModel],
):
    model: Type[MotivatorModel] = MotivatorModel
    entity_cls: Type[MotivatorEntity] = MotivatorEntity

    async def to_entity(self, model: MotivatorModel) -> MotivatorEntity:
        return MotivatorEntity(
            id=model.id,
            idea_id=model.idea_id,
            type=MotivatorTypeEnum(model.type),
            title=model.title,
            description=model.description,
            image_url=model.image_url,
            video_url=model.video_url,
            external_url=model.external_url,
            created_by=model.created_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: MotivatorEntity) -> MotivatorModel:
        payload: dict[str, object] = {
            "idea_id": entity.idea_id,
            "type": str(entity.type),
            "title": entity.title,
            "description": entity.description,
            "image_url": entity.image_url,
            "video_url": entity.video_url,
            "external_url": entity.external_url,
            "created_by": entity.created_by,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(MotivatorEntity, MotivatorTortoiseRepository, RepositoryType.TORTOISE)

