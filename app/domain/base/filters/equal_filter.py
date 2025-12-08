from __future__ import annotations

from abc import ABC
from typing import Set

from domain.base.filters.base_filter import BaseFilterField


class EqualFilterField[T, Q](BaseFilterField[Q], ABC):
    """
    Universal equal / in filter:
        - equal=value      → field = value
        - variants={v1,v2} → field IN (v1, v2)
    """
    equal: T | None = None
    variants: Set[T] | None = None
