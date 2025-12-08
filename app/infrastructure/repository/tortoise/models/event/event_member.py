from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.fields import ForeignKeyRelation

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel

if TYPE_CHECKING:
    from infrastructure.repository.tortoise.models import (
        AccountModel,
        EventModel,
        EventOccurrenceModel,
    )


class EventMemberModel(BaseTortoiseModel):
    """
    Tortoise ORM model for EventMemberEntity.

    Represents a single account participation in a concrete event occurrence.
    """

    # ---------------------------
    # Relations
    # ---------------------------
    event: ForeignKeyRelation[EventModel] = fields.ForeignKeyField(
        "models.EventModel",
        related_name="members",
        on_delete=fields.CASCADE,
        description="Base event.",
    )

    event_occurrence: ForeignKeyRelation[
        EventOccurrenceModel
    ] = fields.ForeignKeyField(
        "models.EventOccurrenceModel",
        related_name="members",
        on_delete=fields.CASCADE,
        description="Concrete occurrence of the event.",
    )

    account: ForeignKeyRelation[AccountModel] = fields.ForeignKeyField(
        "models.AccountModel",
        related_name="event_memberships",
        on_delete=fields.CASCADE,
        description="Account participating in this event occurrence.",
    )

    # ---------------------------
    # State
    # ---------------------------
    has_accepted = fields.BooleanField(
        default=False,
        description="True if user has accepted the participation.",
    )

    # ---------------------------
    # Timestamps (TimestampMixin)
    # ---------------------------
    created_at = fields.DatetimeField(
        auto_now_add=True,
        description="Creation timestamp (UTC).",
    )
    updated_at = fields.DatetimeField(
        auto_now=True,
        description="Last update timestamp (UTC).",
    )

    if TYPE_CHECKING:
        event_id: int
        event_occurrence_id: int
        account_id: int

    class Meta:
        table = "event_members"
        description = "Event occurrence members"
