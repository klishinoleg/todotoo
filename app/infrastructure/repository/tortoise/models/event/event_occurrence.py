from datetime import datetime
from typing import TYPE_CHECKING

from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel

if TYPE_CHECKING:
    from infrastructure.repository.tortoise.models import EventModel, LocationModel


class EventOccurrenceModel(BaseTortoiseModel):
    """
    Tortoise ORM model for EventOccurrenceEntity.

    Represents a single concrete occurrence of an event
    (date/time slot with aggregated state).
    """

    # ---------------------------
    # Relations
    # ---------------------------
    event: fields.ForeignKeyRelation["EventModel"] = fields.ForeignKeyField(
        "models.EventModel",
        related_name="occurrences",
        on_delete=fields.CASCADE,
        description="Base event.",
    )

    location: fields.ForeignKeyNullableRelation["LocationModel"] = fields.ForeignKeyField(
        "models.LocationModel",
        related_name="event_occurrences",
        null=True,
        on_delete=fields.SET_NULL,
        description="Location of this occurrence.",
    )

    # ---------------------------
    # Time window
    # ---------------------------
    start_at = fields.DatetimeField(
        description="Occurrence start datetime (UTC).",
    )
    end_at = fields.DatetimeField(
        description="Occurrence end datetime (UTC).",
    )

    # ---------------------------
    # State
    # ---------------------------
    members_count = fields.IntField(
        default=0,
        description="Cached number of participants.",
    )

    is_canceled = fields.BooleanField(
        default=False,
        description="Whether this occurrence has been canceled.",
    )

    is_finished = fields.BooleanField(
        default=False,
        description="Whether this occurrence has already finished.",
    )

    if TYPE_CHECKING:
        event_id: int
        location_id: int | None

    class Meta:
        table = "event_occurrences"
        description = "Concrete occurrences of events"
