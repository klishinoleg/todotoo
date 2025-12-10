from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType, FilterFieldType
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

        if self.is_null is not None:
            query = query.filter(**{f"{name}__isnull": self.is_null})

        return query


DIRepository.register_filter(FilterFieldType.RANGE, TortoiseRangeFilterField, RepositoryType.TORTOISE)
