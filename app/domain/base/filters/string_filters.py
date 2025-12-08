from __future__ import annotations
from abc import ABC

from domain.base.filters.base_filter import BaseFilterField


class StringEqualFilterField[Q](BaseFilterField[Q], ABC):
    value: str


class StringContainsFilterField[Q](BaseFilterField[Q], ABC):
    value: str


class StringStartsWithFilterField[Q](BaseFilterField[Q], ABC):
    value: str


class StringEndsWithFilterField[Q](BaseFilterField[Q], ABC):
    value: str
