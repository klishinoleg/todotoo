from __future__ import annotations

from dataclasses import asdict
from typing import Any, get_args, get_origin

from application.base.dto.crud import CrudListResponseDTO
from application.base.service.base_service import BaseService
from core.di.repository import DIRepository
from core.enums.di.repository import FilterFieldType
from core.enums.system.error_fields import ErrorFields
from core.exceptions.system import RepositoryException
from domain.base.entity import BaseEntity
from domain.base.exceptions import DomainValidationException
from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.bool_filter import BoolFilterField
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.range_filter import RangeFilterField
from domain.base.filters.string_filters import TextFilterField
from domain.base.repository import BaseRepository


class CrudEntityNotFound(DomainValidationException):
    pass


class BaseCrudUseCase[E: BaseEntity, FD: BaseFilter]:
    """
    Generic CRUD use case for any domain entity with registered repository.
    """

    def __init__(self, entity_cls: type[E], filter_cls: type[FD], account: Any = None) -> None:
        self._entity_cls = entity_cls
        self._filter_cls = filter_cls
        self.account = account
        self._service: BaseService[E, FD, BaseRepository] = BaseService(entity_cls)

    async def list(self, filter_payload: dict[str, Any]) -> CrudListResponseDTO:
        filters = self._build_filter(filter_payload)
        entities = await self._service.filtered_list(filters)
        total = await self._service.filtered_count(filters)

        page = filters.page or 1
        per_page = filters.per_page if filters.per_page is not None else len(entities)

        return CrudListResponseDTO(
            items=[self._serialize_entity(entity) for entity in entities],
            total=total,
            page=page,
            per_page=per_page,
        )

    async def get(self, entity_id: int) -> dict[str, Any]:
        entity = await self._get_or_raise(entity_id)
        return self._serialize_entity(entity)

    async def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        create_payload = dict(payload)
        create_payload.pop("id", None)
        try:
            entity = self._entity_cls(**create_payload)
        except TypeError as exc:
            raise DomainValidationException(str(exc), field=ErrorFields.DETAILS)

        created = await self._service.create(entity)
        return self._serialize_entity(created)

    async def update(self, entity_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        entity = await self._get_or_raise(entity_id)

        allowed_fields = set(entity.to_dict().keys()) - {"id"}
        updates = {key: value for key, value in payload.items() if key in allowed_fields}

        if not updates:
            return self._serialize_entity(entity)

        try:
            updated_entity = entity.get_new_updated(updates)
        except TypeError as exc:
            raise DomainValidationException(str(exc), field=ErrorFields.DETAILS)

        saved = await self._service.save(updated_entity, update_fields=set(updates.keys()))
        return self._serialize_entity(saved)

    async def delete(self, entity_id: int) -> bool:
        entity = await self._service.get(entity_id)
        if not entity:
            raise CrudEntityNotFound(
                f"{self._entity_cls.__name__} with id={entity_id} was not found",
                field=ErrorFields.DETAILS,
            )
        return await self._service.delete(entity_id)

    def _build_filter(self, filter_payload: dict[str, Any]) -> FD:
        normalized_payload = self._normalize_filter_payload(filter_payload)
        try:
            return self._filter_cls.model_construct(**normalized_payload)
        except Exception as exc:
            raise DomainValidationException(str(exc), field=ErrorFields.DETAILS)

    def _normalize_filter_payload(self, filter_payload: dict[str, Any]) -> dict[str, Any]:
        normalized: dict[str, Any] = dict(filter_payload)

        for field_name, model_field in self._filter_cls.model_fields.items():
            if field_name not in normalized:
                continue

            raw_value = normalized[field_name]
            if raw_value is None:
                continue

            filter_field_cls = self._resolve_filter_field_class(model_field.annotation)
            if filter_field_cls is None:
                continue

            prepared_value: Any = raw_value

            if issubclass(filter_field_cls, BoolFilterField):
                if not isinstance(prepared_value, dict):
                    prepared_value = {"value": bool(prepared_value)}
                normalized[field_name] = self._instantiate_filter_field(FilterFieldType.BOOLEAN, prepared_value)
                continue

            if issubclass(filter_field_cls, EqualFilterField):
                if not isinstance(prepared_value, dict):
                    if isinstance(prepared_value, (list, tuple, set)):
                        prepared_value = {"variants": list(prepared_value)}
                    else:
                        prepared_value = {"equal": prepared_value}
                normalized[field_name] = self._instantiate_filter_field(FilterFieldType.EQUAL, prepared_value)
                continue

            if issubclass(filter_field_cls, RangeFilterField):
                if not isinstance(prepared_value, dict):
                    if isinstance(prepared_value, (list, tuple)) and len(prepared_value) == 2:
                        prepared_value = {"from_value": prepared_value[0], "to_value": prepared_value[1]}
                    else:
                        prepared_value = {"equal": prepared_value}
                normalized[field_name] = self._instantiate_filter_field(FilterFieldType.RANGE, prepared_value)
                continue

            if issubclass(filter_field_cls, TextFilterField):
                if not isinstance(prepared_value, dict):
                    prepared_value = {"contains": str(prepared_value)}
                normalized[field_name] = self._instantiate_filter_field(FilterFieldType.TEXT, prepared_value)
                continue

            normalized[field_name] = prepared_value

        return normalized

    @staticmethod
    def _instantiate_filter_field(filter_field_type: FilterFieldType, value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        try:
            filter_impl = DIRepository.get_filter(filter_field_type)
            return filter_impl.model_validate(value)
        except RepositoryException:
            return value
        except Exception:
            return value

    @staticmethod
    def _resolve_filter_field_class(annotation: Any) -> type | None:
        origin = get_origin(annotation)
        args = get_args(annotation)

        if origin is None:
            if isinstance(annotation, type):
                return annotation
            return None

        for arg in args:
            if arg is type(None):
                continue
            if isinstance(arg, type):
                return arg

        return None

    async def _get_or_raise(self, entity_id: int) -> E:
        entity = await self._service.get(entity_id)
        if not entity:
            raise CrudEntityNotFound(
                f"{self._entity_cls.__name__} with id={entity_id} was not found",
                field=ErrorFields.DETAILS,
            )
        return entity

    @staticmethod
    def _serialize_entity(entity: BaseEntity) -> dict[str, Any]:
        if hasattr(entity, "to_dict"):
            return entity.to_dict()
        return asdict(entity)
