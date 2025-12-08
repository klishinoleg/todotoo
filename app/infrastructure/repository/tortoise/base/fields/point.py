from __future__ import annotations

from typing import Any

from tortoise import fields, Model
from postgis import Point

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class PostGISPointField(fields.Field):
    SQL_TYPE = "geometry(Point, 4326)"

    def to_db_value(self, value: Any, instance: type[Model] | Model) -> Any:
        """
        Convert Python Point → DB representation.
        Must keep the same signature as the parent class.
        """
        if value is None:
            return None

        if not isinstance(value, Point):
            raise TypeError(f"Expected Point, got {type(value)}")

        # EWKB returns bytes → DB accepts bytes
        return value.to_ewkb()

    def to_python_value(self, value: Any) -> Point | None:
        """
        Convert DB value (EWKB or WKB hex) → Python Point.
        """
        if value is None:
            return None

        return Point.from_ewkb(value)
