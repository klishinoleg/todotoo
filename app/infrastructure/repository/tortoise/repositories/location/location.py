from __future__ import annotations

from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from core.storage import get_storage
from domain.location.entities.location import LocationEntity
from domain.location.repositories.location import LocationFilter, LocationRepository
from infrastructure.repository.tortoise.base.geo.convert import (
    to_postgis_point,
    to_postgis_polygon, from_postgis_point, from_postgis_polygon,
)
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.location.location import LocationModel


class LocationTortoiseRepository(
    LocationRepository[QuerySet],
    BaseTortoiseRepository[LocationEntity, LocationFilter[QuerySet], LocationModel],
):
    """
    Tortoise ORM repository for LocationEntity.

    Uses:
        - PostGIS Point for `point`
        - PostGIS Geometry for `geometry`
    """

    model: Type[LocationModel] = LocationModel
    entity_cls: Type[LocationEntity] = LocationEntity

    # ---------------------------------------
    # Mapping: Model → Entity
    # ---------------------------------------
    async def to_entity(self, model: LocationModel) -> LocationEntity:
        storage = get_storage()
        image = storage.get_url(model.image)
        return LocationEntity(
            id=model.id,
            name=model.name,
            type=model.type,
            point=from_postgis_point(model.point),
            polygon=from_postgis_polygon(model.polygon),
            address_raw=model.address_raw,
            address_structured=model.address_structured,
            parent_id=model.parent_id,
            image=image,
            image_small=image,
            image_medium=image,
            image_large=image,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    # ---------------------------------------
    # Mapping: Entity → Model for DB insert/update
    # ---------------------------------------
    def from_entity(self, entity: LocationEntity) -> LocationModel:
        storage = get_storage()
        payload: dict[str, object] = {
            "name": entity.name,
            "type": entity.type,
            "point": to_postgis_point(entity.point),
            "polygon": to_postgis_polygon(entity.polygon),
            "address_raw": entity.address_raw,
            "address_structured": entity.address_structured,
            "parent_id": entity.parent_id,
            "image": storage.to_key(entity.image),
            "is_active": entity.is_active,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


# Register concrete repository in DI
DIRepository.register(LocationEntity, LocationTortoiseRepository, RepositoryType.TORTOISE)
