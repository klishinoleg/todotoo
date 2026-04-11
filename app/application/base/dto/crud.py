from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CrudPayloadDTO(BaseModel):
    model_config = ConfigDict(extra="allow")
    data: dict[str, Any] = Field(default_factory=dict)


class CrudListResponseDTO(BaseModel):
    items: list[dict[str, Any]]
    total: int
    page: int
    per_page: int


class CrudDeleteResponseDTO(BaseModel):
    success: bool
