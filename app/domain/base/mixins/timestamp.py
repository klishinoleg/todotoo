from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from abc import ABC
from typing import Self

from core.helpers.func.date_time import get_utc_time


@dataclass
class TimestampMixin(ABC):
    created_at: datetime = field(default_factory=get_utc_time, repr=False)
    updated_at: datetime = field(default_factory=get_utc_time, repr=False)

    def get_new_with_updated_time(self) -> Self:
        """Return new instance with updated timestamp."""
        return replace(self, updated_at=get_utc_time())
