from __future__ import annotations

from typing import Any
from tortoise import fields

from postgis import Polygon


class PostGISPolygonField(fields.Field):
    SQL_TYPE = "geometry(Polygon, 4326)"

    def to_db_value(self, value: Any, instance: Any) -> Any:
        """
        Convert Python Polygon → DB EWKB bytes.
        Must keep same signature as parent class for LSP.
        """
        if value is None:
            return None

        if not isinstance(value, Polygon):
            raise TypeError(f"Expected Polygon, got {type(value)}")

        return value.to_ewkb()

    def to_python_value(self, value: Any) -> Polygon | None:
        """
        Convert DB EWKB → Python Polygon.
        """
        if value is None:
            return None

        return Polygon.from_ewkb(value)
