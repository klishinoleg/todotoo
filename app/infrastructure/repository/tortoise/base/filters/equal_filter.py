from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType, FilterFieldType
from domain.base.filters.equal_filter import EqualFilterField


class TortoiseEqualFilterField[T](EqualFilterField[T, QuerySet]):
    """
    Tortoise equal/in filter.

    Examples:

    equal=5
        → .filter(field=5)

    variants={1,2,3}
        → .filter(field__in=[1,2,3])
    """

    def extend_query(self, name: str, query: QuerySet) -> QuerySet:
        # exact equality
        if self.equal is not None:
            return query.filter(**{name: self.equal})

        # list of possible values
        if self.variants:
            return query.filter(**{f"{name}__in": list(self.variants)})

        # no filtering applied
        return query


DIRepository.register_filter(FilterFieldType.EQUAL, TortoiseEqualFilterField, RepositoryType.TORTOISE)
