from typing import TYPE_CHECKING

from tortoise import fields

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel

if TYPE_CHECKING:
    from infrastructure.repository.tortoise.models.account.account import AccountModel


class AccountSessionModel(BaseTortoiseModel):
    """
    Tortoise ORM model for AccountSessionEntity.

    Tracks:
        - account owning this session
        - requests counter
        - start / close timestamps
    """

    account: fields.ForeignKeyRelation["AccountModel"] = fields.ForeignKeyField(
        "models.AccountModel", related_name="sessions", on_delete=fields.CASCADE)
    requests = fields.IntField(default=0)

    started_at = fields.DatetimeField(auto_now_add=True)
    closed_at = fields.DatetimeField(null=True)

    if TYPE_CHECKING:
        account_id: int

    class Meta:
        table = "account_sessions"
