from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, Field
from starlette.requests import Request


class ReactAdminFilter(BaseModel):
    filter: dict[str, Any] = Field(default_factory=dict)
    sort: tuple[str, str] | None = None
    range: tuple[int, int] | None = None

    @classmethod
    def from_request(cls, request: Request) -> "ReactAdminFilter":
        query = request.query_params
        return cls(
            filter=cls._parse_json_param(query.get("filter"), default={}),
            sort=cls._parse_tuple_param(query.get("sort")),
            range=cls._parse_tuple_param(query.get("range")),
        )

    @staticmethod
    def _parse_json_param(raw_value: str | None, default: Any) -> Any:
        if raw_value is None:
            return default
        return json.loads(raw_value)

    @staticmethod
    def _parse_tuple_param(raw_value: str | None) -> tuple[Any, Any] | None:
        if raw_value is None:
            return None
        loaded = json.loads(raw_value)
        if not isinstance(loaded, list) or len(loaded) != 2:
            return None
        return loaded[0], loaded[1]

    def apply_aliases(self, aliases: dict[str, str]) -> None:
        if not aliases:
            return

        remapped: dict[str, Any] = {}
        for raw_key, value in self.filter.items():
            if "___" in raw_key:
                field, _, op = raw_key.rpartition("___")
                mapped_field = aliases.get(field, field)
                mapped_key = f"{mapped_field}___{op}"
            else:
                mapped_key = aliases.get(raw_key, raw_key)
            remapped[mapped_key] = value

        self.filter = remapped

    def to_filter_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = dict(self.filter)

        if self.sort:
            field_name, direction = str(self.sort[0]), str(self.sort[1]).upper()
            payload["order_data"] = [f"-{field_name}" if direction == "DESC" else field_name]

        if self.range:
            start, end = int(self.range[0]), int(self.range[1])
            if end >= start:
                per_page = end - start + 1
                payload["page"] = start // per_page + 1
                payload["per_page"] = per_page

        return payload
