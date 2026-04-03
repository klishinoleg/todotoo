from functools import lru_cache

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class MediaTypeEnum(BaseLabeledEnum):
    IMAGE = "image"
    VIDEO = "video"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.IMAGE: _("Image"),
            cls.VIDEO: _("Video"),
        }

