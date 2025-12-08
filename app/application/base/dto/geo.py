from typing import Literal
from pydantic import BaseModel
from core.enums.app.location.geometry_type import GeometryType
from domain.base.value_objects.geometry import GeometryPoint, GeometryPolygon


class GeometryPointDTO(BaseModel):
    """
    DTO representation of a point geometry.
    Matches GeometryPoint domain value object.
    """
    type: Literal[GeometryType.POINT]
    latitude: float
    longitude: float


class GeometryPolygonDTO(BaseModel):
    """
    DTO representation of a polygon geometry.
    Matches GeometryPolygon domain value object.
    points is a list of (lat, lng) tuples.
    """
    type: Literal[GeometryType.POLYGON]
    points: list[tuple[float, float]]
