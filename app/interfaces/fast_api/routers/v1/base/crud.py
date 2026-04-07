from __future__ import annotations

from abc import ABC
from enum import Enum
from typing import Any, Protocol, cast

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from starlette.requests import Request

from application.base.dto.crud import CrudDeleteResponseDTO, CrudListResponseDTO, CrudPayloadDTO
from application.base.use_case.crud import CrudEntityNotFound
from core.exceptions.system import RepositoryException
from domain.account.entities.account import AccountEntity
from domain.base.exceptions import DomainValidationException
from interfaces.fast_api.deps.account import get_current_account
from interfaces.fast_api.routers.v1.base.filter import ReactAdminFilter


class CrudRouterUseCaseProtocol(Protocol):
    async def list(self, filter_payload: dict[str, Any]) -> CrudListResponseDTO:
        ...

    async def get(self, entity_id: int) -> dict[str, Any]:
        ...

    async def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...

    async def update(self, entity_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        ...

    async def delete(self, entity_id: int) -> bool:
        ...


class V1CrudRouter[UC: CrudRouterUseCaseProtocol](ABC):
    prefix: str
    tags: list[str | Enum] = ["v1-crud"]
    use_case_cls: type[Any]

    create_payload_model: type[BaseModel] = CrudPayloadDTO
    update_payload_model: type[BaseModel] = CrudPayloadDTO

    def __init__(self) -> None:
        self.router = APIRouter(prefix=self.prefix, tags=self.tags)
        self._register_standard_routes()
        self.register_custom_routes()

    def get_use_case(self, account: AccountEntity) -> UC:
        return cast(UC, cast(Any, self.use_case_cls)(account))

    def get_filter_aliases(self) -> dict[str, str]:
        return {}

    def register_custom_routes(self) -> None:
        return None

    def _register_standard_routes(self) -> None:
        router = self.router
        create_payload_model = self.create_payload_model
        update_payload_model = self.update_payload_model

        @router.get("/", response_model=CrudListResponseDTO)
        async def list_items(
                request: Request,
                account: AccountEntity = Depends(get_current_account),
        ) -> CrudListResponseDTO:
            try:
                ra_filter = ReactAdminFilter.from_request(request)
                ra_filter.apply_aliases(self.get_filter_aliases())
                use_case = self.get_use_case(account)
                return await use_case.list(ra_filter.to_filter_payload())
            except DomainValidationException as exc:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)
            except RepositoryException as exc:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=str(exc))

        @router.get("/{entity_id}/", response_model=dict[str, Any])
        async def get_item(
                entity_id: int,
                account: AccountEntity = Depends(get_current_account),
        ) -> dict[str, Any]:
            try:
                use_case = self.get_use_case(account)
                return await use_case.get(entity_id)
            except CrudEntityNotFound as exc:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
            except DomainValidationException as exc:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)
            except RepositoryException as exc:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=str(exc))

        @router.post("/", response_model=dict[str, Any], status_code=status.HTTP_201_CREATED)
        async def create_item(
                data: create_payload_model,  # type: ignore
                account: AccountEntity = Depends(get_current_account),
        ) -> dict[str, Any]:
            try:
                use_case = self.get_use_case(account)
                payload = cast(BaseModel, data).model_dump()
                if "data" in payload and isinstance(payload["data"], dict):
                    payload = payload["data"]
                return await use_case.create(payload)
            except DomainValidationException as exc:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)
            except RepositoryException as exc:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=str(exc))

        @router.put("/{entity_id}/", response_model=dict[str, Any])
        async def update_item(
                entity_id: int,
                data: update_payload_model,  # type: ignore
                account: AccountEntity = Depends(get_current_account),
        ) -> dict[str, Any]:
            try:
                use_case = self.get_use_case(account)
                payload = cast(BaseModel, data).model_dump(exclude_unset=True)
                if "data" in payload and isinstance(payload["data"], dict):
                    payload = payload["data"]
                return await use_case.update(entity_id, payload)
            except CrudEntityNotFound as exc:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
            except DomainValidationException as exc:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)
            except RepositoryException as exc:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=str(exc))

        @router.delete("/{entity_id}/", response_model=CrudDeleteResponseDTO)
        async def delete_item(
                entity_id: int,
                account: AccountEntity = Depends(get_current_account),
        ) -> CrudDeleteResponseDTO:
            try:
                use_case = self.get_use_case(account)
                success = await use_case.delete(entity_id)
                return CrudDeleteResponseDTO(success=success)
            except CrudEntityNotFound as exc:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
            except DomainValidationException as exc:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)
            except RepositoryException as exc:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=str(exc))
