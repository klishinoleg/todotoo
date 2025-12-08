from typing import TYPE_CHECKING

from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel
from core.enums.app.account.auth_provider import AuthProviderType

if TYPE_CHECKING:
    from infrastructure.repository.tortoise.models.account.account import AccountModel


class AccountAuthProfileModel(BaseTortoiseModel):
    """
    Tortoise ORM model for account authentication profiles.

    Stores external authentication provider bindings for a user account
    (e.g. Google, Apple, etc.).
    """

    account: fields.ForeignKeyRelation["AccountModel"] = fields.ForeignKeyField(
        "models.AccountModel",
        related_name="auth_profiles",
        description="Related account ID",
        on_delete=fields.CASCADE,
    )

    provider_type: AuthProviderType = fields.CharEnumField(
        AuthProviderType,
        description="Authentication provider type (google, apple, etc.)",
    )

    provider_id = fields.CharField(
        max_length=255,
        index=True,
        description="Provider-specific identifier (e.g. sub/uid).",
    )

    provider_data: dict = fields.JSONField(
        null=False,
        default=dict,
        description="Raw provider profile / tokens (provider-specific schema).",
    )

    language_code = fields.CharField(
        max_length=10,
        null=True,
        description="Preferred language reported by provider or user.",
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

    if TYPE_CHECKING:
        account_id: int

    class Meta:
        table = "account_auth_profile"
        unique_together = ("provider_type", "provider_id")
        description = "External authentication profiles for accounts"
