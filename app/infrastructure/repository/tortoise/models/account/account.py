from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class AccountModel(BaseTortoiseModel):
    """
    Tortoise ORM model for user accounts.

    Mirrors AccountEntity fields.
    """

    # Required
    username = fields.CharField(max_length=150, unique=True)
    public_name = fields.CharField(max_length=150, null=True)

    email = fields.CharField(max_length=255, null=True)
    language = fields.CharField(max_length=16, default="en")

    is_online = fields.BooleanField(default=False)

    avatar = fields.CharField(max_length=1024, null=True)

    # Mixins
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "accounts"
