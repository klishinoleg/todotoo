from __future__ import annotations

from pydantic import BaseModel


class EnumItemDTO(BaseModel):
    id: str
    name: str


class EnumsConfigDTO(BaseModel):
    version: str
    language: str
    supported_languages: list[str]
    enums: dict[str, list[EnumItemDTO]]
