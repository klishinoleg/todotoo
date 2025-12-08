from typing import TYPE_CHECKING, Callable, Awaitable

from tortoise import fields
from tortoise_imagefield import ImageField

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

    avatar = ImageField(directory_name="avatars", field_for_name="username")

    # Mixins
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    is_active = fields.BooleanField(default=True)

    if TYPE_CHECKING:
        get_avatar_url: Callable[[], str]
        get_avatar_webp: Callable[[int, int, str, bool | None], Awaitable[str]]

    class Meta:
        table = "accounts"
