from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.base.filters.range_filter import RangeFilterField


class TortoiseRangeFilterField[T](RangeFilterField[T, QuerySet]):
    """
    Tortoise ORM range filter for numeric or datetime fields.
    """

    def extend_query(self, name: str, query: QuerySet) -> QuerySet:
        # Equal has highest priority
        if self.equal is not None:
            return query.filter(**{name: self.equal})

        # From
        if self.from_value is not None:
            query = query.filter(**{f"{name}__gte": self.from_value})

        # To
        if self.to_value is not None:
            query = query.filter(**{f"{name}__lte": self.to_value})

        return query


DIRepository.register_filter(TortoiseRangeFilterField, RepositoryType.TORTOISE)
