from functools import lru_cache

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class MotivatorTypeEnum(BaseLabeledEnum):
    IMAGE = "image"
    YOUTUBE = "youtube"
    ARTICLE = "article"
    TEXT = "text"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.IMAGE: _("Image"),
            cls.YOUTUBE: _("YouTube"),
            cls.ARTICLE: _("Article"),
            cls.TEXT: _("Text"),
        }

