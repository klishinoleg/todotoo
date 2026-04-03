from dataclasses import dataclass


@dataclass(slots=True, kw_only=True, frozen=True)
class GeoPoint:
    latitude: float
    longitude: float
    address: str | None = None

