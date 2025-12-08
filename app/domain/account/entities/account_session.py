from dataclasses import dataclass, field
from datetime import datetime

from core.helpers.func.date_time import get_utc_time
from domain.base.entity import BaseEntity


@dataclass(slots=True, kw_only=True)
class AccountSessionEntity(BaseEntity):
    """
    Represents a minimal login session for an account.

    Tracks:
        - When the user became online (started_at)
        - When they went offline (closed_at)
        - How many requests were made during session
    """

    account_id: int
    requests: int = 0

    started_at: datetime = field(default_factory=get_utc_time)
    closed_at: datetime | None = None

    # ---------------------------------------
    # Domain behavior
    # ---------------------------------------

    def close(self, dt: datetime | None = None) -> "AccountSessionEntity":
        """Return new entity with session closed."""
        return self.get_new_updated({
            "closed_at": dt or get_utc_time()
        })

    def increment_requests(self) -> "AccountSessionEntity":
        """Return new entity with incremented request counter."""
        return self.get_new_updated({
            "requests": self.requests + 1
        })
