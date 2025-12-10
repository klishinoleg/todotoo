from tortoise.queryset import QuerySet
from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType, FilterFieldType
from domain.base.filters.string_filters import TextFilterField


class TortoiseTextFilterField(TextFilterField[QuerySet]):
    """field ILIKE %value%"""

    def extend_query(self, name: str, query: QuerySet) -> QuerySet:
        if self.contains is not None:
            return query.filter(**{f"{name}__icontains": self.contains})
        if self.start is not None:
            return query.filter(**{f"{name}__istartswith": self.start})
        if self.end is not None:
            return query.filter(**{f"{name}__iendswith": self.end})
        return query


DIRepository.register_filter(FilterFieldType.TEXT, TortoiseTextFilterField, RepositoryType.TORTOISE)
