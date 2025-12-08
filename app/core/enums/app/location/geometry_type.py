from functools import lru_cache
from typing import Self

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class GeometryType(BaseLabeledEnum):
    POINT = "point"
    CIRCLE = "circle"
    POLYGON = "polygon"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.POINT: _("Point"),
            cls.CIRCLE: _("Circle"),
            cls.POLYGON: _("Polygon"),
        }
