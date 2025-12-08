from dataclasses import dataclass, field, replace
from abc import ABC
from typing import Self


@dataclass
class WithActiveMixin(ABC):
    is_active: bool = True

    def get_new_activated(self) -> Self:
        return replace(self, is_active=True)

    def get_new_deactivated(self) -> Self:
        return replace(self, is_active=False)
