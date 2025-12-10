from __future__ import annotations
from abc import ABC

from domain.base.filters.base_filter import BaseFilterField


class TextFilterField[Q](BaseFilterField[Q], ABC):
    contains: str | None = None
    start: str | None = None
    end: str | None = None
