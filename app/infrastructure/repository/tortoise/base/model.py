from tortoise import fields
from tortoise.models import Model


class BaseTortoiseModel(Model):
    """
    Base Tortoise model with only ID.
    Every Tortoise ORM model in the project must inherit this.
    """
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True
