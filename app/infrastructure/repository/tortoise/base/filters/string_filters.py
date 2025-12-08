from tortoise.queryset import QuerySet
from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.base.filters.string_filters import StringEqualFilterField, StringContainsFilterField, \
    StringStartsWithFilterField, StringEndsWithFilterField


class TortoiseStringEqualFilterField(StringEqualFilterField[QuerySet]):
    """field = value"""

    def extend_query(self, name: str, query: QuerySet) -> QuerySet:
        return query.filter(**{name: self.value})


class TortoiseStringContainsFilterField(StringContainsFilterField[QuerySet]):
    """field ILIKE %value%"""

    def extend_query(self, name: str, query: QuerySet) -> QuerySet:
        return query.filter(**{f"{name}__icontains": self.value})


class TortoiseStringStartsWithFilterField(StringStartsWithFilterField[QuerySet]):
    """field ILIKE value%"""

    def extend_query(self, name: str, query: QuerySet) -> QuerySet:
        return query.filter(**{f"{name}__istartswith": self.value})


class TortoiseStringEndsWithFilterField(StringEndsWithFilterField[QuerySet]):
    """field ILIKE %value"""

    def extend_query(self, name: str, query: QuerySet) -> QuerySet:
        return query.filter(**{f"{name}__iendswith": self.value})


DIRepository.register_filter(TortoiseStringEqualFilterField, RepositoryType.TORTOISE)
DIRepository.register_filter(TortoiseStringContainsFilterField, RepositoryType.TORTOISE)
DIRepository.register_filter(TortoiseStringStartsWithFilterField, RepositoryType.TORTOISE)
DIRepository.register_filter(TortoiseStringEndsWithFilterField, RepositoryType.TORTOISE)
