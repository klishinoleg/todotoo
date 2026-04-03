from __future__ import annotations

from abc import ABCMeta, abstractmethod
from enum import EnumMeta, StrEnum
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
    def _label_map(cls) -> Dict[str, str]:
        raise NotImplementedError

    @classmethod
    def choices(cls) -> Tuple[Tuple[str, str], ...]:
        """
        Returns tuple of (value, label) pairs.
        value is always str because StrEnum.
        """
        cls._clear_label_cache()
        return tuple((str(key), val) for key, val in cls._label_map().items())

    def get_label(self) -> str:
        """
        Returns human-readable label for this enum member.
        """
        self.__class__._clear_label_cache()
        return self._label_map()[self]

    @classmethod
    def _clear_label_cache(cls) -> None:
        clear_fn = getattr(cls._label_map, "cache_clear", None)
        if clear_fn:
            clear_fn()
