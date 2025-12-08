from __future__ import annotations

from abc import ABC

from domain.base.filters.base_filter import BaseFilterField


class RangeFilterField[T, Q](BaseFilterField[Q], ABC):
    """Universal range filter: from_value <= field <= to_value."""
    from_value: T | None = None
    to_value: T | None = None
    equal: T | None = None
