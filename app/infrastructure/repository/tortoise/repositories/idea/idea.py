from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from core.enums.app.idea.status import IdeaStatusEnum
from core.enums.app.idea.visibility import IdeaVisibilityEnum
from domain.idea.entities.idea import IdeaEntity
from domain.idea.repositories.idea import IdeaFilter, IdeaRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.idea.idea import IdeaModel


class IdeaTortoiseRepository(
    IdeaRepository[QuerySet],
    BaseTortoiseRepository[IdeaEntity, IdeaFilter[QuerySet], IdeaModel],
):
    model: Type[IdeaModel] = IdeaModel
    entity_cls: Type[IdeaEntity] = IdeaEntity

    async def to_entity(self, model: IdeaModel) -> IdeaEntity:
        return IdeaEntity(
            id=model.id,
            title=model.title,
            description=model.description,
            slogan=model.slogan,
            cover_image=model.cover_image,
            creator_id=model.creator_id,
            visibility=IdeaVisibilityEnum(model.visibility),
            status=IdeaStatusEnum(model.status),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: IdeaEntity) -> IdeaModel:
        payload: dict[str, object] = {
            "title": entity.title,
            "description": entity.description,
            "slogan": entity.slogan,
            "cover_image": entity.cover_image,
            "creator_id": entity.creator_id,
            "visibility": str(entity.visibility),
            "status": str(entity.status),
            "is_active": entity.is_active,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(IdeaEntity, IdeaTortoiseRepository, RepositoryType.TORTOISE)

