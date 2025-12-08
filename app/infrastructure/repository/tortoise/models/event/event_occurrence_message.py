from typing import TYPE_CHECKING

from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel

if TYPE_CHECKING:
    from infrastructure.repository.tortoise.models import (
        EventModel,
        EventOccurrenceModel,
        EventMemberModel,
    )


class EventOccurrenceMessageModel(BaseTortoiseModel):
    """
    Tortoise ORM model for EventOccurrenceMessageEntity.

    Represents a single chat/message item inside an event occurrence thread.
    """

    # ---------------------------
    # Relations
    # ---------------------------
    event: fields.ForeignKeyRelation[EventModel] = fields.ForeignKeyField(
        "models.EventModel",
        related_name="messages",
        on_delete=fields.CASCADE,
        description="Parent event.",
    )

    event_occurrence: fields.ForeignKeyRelation["EventOccurrenceModel"] = fields.ForeignKeyField(
        "models.EventOccurrenceModel",
        related_name="messages",
        on_delete=fields.CASCADE,
        description="Concrete event occurrence.",
    )

    parent_message: fields.ForeignKeyNullableRelation["EventOccurrenceMessageModel"] = fields.ForeignKeyField(
        "models.EventOccurrenceMessageModel",
        related_name="replies",
        null=True,
        on_delete=fields.SET_NULL,
        description="Optional parent message (for threads).",
    )

    event_member: fields.ForeignKeyNullableRelation[EventMemberModel] = fields.ForeignKeyField(
        "models.EventMemberModel",
        related_name="messages",
        null=True,
        on_delete=fields.SET_NULL,
        description="Author membership within occurrence (optional).",
    )

    # ---------------------------
    # Payload
    # ---------------------------
    text = fields.TextField(
        description="Message text.",
    )

    image = fields.CharField(
        max_length=512,
        null=True,
        description="Optional image URL attached to message.",
    )

    # ---------------------------
    # Mixins: TimestampMixin + WithActiveMixin
    # ---------------------------
    created_at = fields.DatetimeField(
        auto_now_add=True,
        description="Creation timestamp (UTC).",
    )
    updated_at = fields.DatetimeField(
        auto_now=True,
        description="Last update timestamp (UTC).",
    )
    is_active = fields.BooleanField(
        default=True,
        description="Logical active flag (soft delete / hide).",
    )

    if TYPE_CHECKING:
        event_id: int
        event_occurrence_id: int
        parent_message_id: int | None
        event_member_id: int | None

    class Meta:
        table = "event_occurrence_messages"
        description = "Messages inside event occurrences"
