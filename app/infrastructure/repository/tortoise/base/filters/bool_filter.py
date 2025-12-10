from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType, FilterFieldType
from domain.base.filters.bool_filter import BoolFilterField


class TortoiseBoolFilterField(BoolFilterField[QuerySet]):
    """
    Boolean filter for Tortoise ORM.

    Example:
        is_active=True -> query.filter(is_active=True)
    """

    def extend_query(self, name: str, query: QuerySet) -> QuerySet:
        return query.filter(**{name: self.value})


DIRepository.register_filter(FilterFieldType.BOOLEAN, TortoiseBoolFilterField, RepositoryType.TORTOISE)
