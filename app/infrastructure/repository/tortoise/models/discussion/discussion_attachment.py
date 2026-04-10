from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class DiscussionAttachmentModel(BaseTortoiseModel):
    message_id = fields.IntField(index=True)
    file_url = fields.CharField(max_length=1024)
    file_type = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "discussion_attachments"

