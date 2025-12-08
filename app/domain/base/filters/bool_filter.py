from __future__ import annotations

from abc import ABC

from domain.base.filters.base_filter import BaseFilterField


class BoolFilterField[Q](BaseFilterField[Q], ABC):
    """true / false"""
    value: bool
