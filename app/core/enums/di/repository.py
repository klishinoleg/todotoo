from enum import StrEnum


class RepositoryType(StrEnum):
    TORTOISE = "tortoise"
    MOCK = "mock"


class FilterFieldType(StrEnum):
    BOOLEAN = "boolean"
    EQUAL = "equal"
    RANGE = "range"
    GEOMETRY = "geometry"
    TEXT = "text"
