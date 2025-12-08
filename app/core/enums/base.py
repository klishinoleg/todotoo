from __future__ import annotations

from abc import ABCMeta, abstractmethod
from enum import EnumMeta, StrEnum
from functools import lru_cache
from typing import Dict, Tuple


class ABCEnumMeta(EnumMeta, ABCMeta):
    """
    Metaclass combining EnumMeta and ABCMeta to allow abstract enum classes.
    """
    pass


class BaseLabeledEnum(StrEnum, metaclass=ABCEnumMeta):
    """
    Base enum class that supports label mapping and choices().
    Child enums must implement _label_map().
    """

    # Child classes must return mapping: member -> label
    @classmethod
    @abstractmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> Dict[str, str]:
        raise NotImplementedError

    @classmethod
    @lru_cache(maxsize=1)
    def choices(cls) -> Tuple[Tuple[str, str], ...]:
        """
        Returns tuple of (value, label) pairs.
        value is always str because StrEnum.
        """
        return tuple((key, val) for key, val in cls._label_map().items())

    def get_label(self) -> str:
        """
        Returns human-readable label for this enum member.
        """
        return self._label_map()[self]
