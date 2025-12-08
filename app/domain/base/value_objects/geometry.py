from abc import ABC, abstractmethod
from dataclasses import dataclass
from core.enums.app.location.geometry_type import GeometryType


class BaseGeometry(ABC):
    geometry_type: GeometryType

    @abstractmethod
    def to_dict(self) -> dict:
        ...


@dataclass(slots=True, kw_only=True)
class GeometryPoint(BaseGeometry):
    type = GeometryType.POINT
    latitude: float
    longitude: float

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "coordinates": [self.longitude, self.latitude],
        }


@dataclass(slots=True, kw_only=True)
class GeometryPolygon(BaseGeometry):
    points: list[tuple[float, float]]  # (lat, lng)
    type = GeometryType.POLYGON

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "coordinates": [
                [(lng, lat) for lat, lng in self.points]
            ],
        }
