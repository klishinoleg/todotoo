from typing import Callable, TypeVar

E = TypeVar("E")  # Enum type
R = TypeVar("R")  # Result type


def safe_enum_match(
        value: E,
        cases: dict[E, Callable[[], R]],
        default: Callable[[], R] | None = None
) -> R:
    """
    Safe enum matcher that behaves like switch-case for enums.

    Args:
        value: enum value to match
        cases: dictionary of enum value -> handler function
        default: optional default handler if no case matches

    Returns:
        Result of matched handler

    Raises:
        ValueError if no match found and no default provided.
    """
    handler = cases.get(value)
    if handler is not None:
        return handler()
    if default is not None:
        return default()
    raise ValueError(f"Unhandled enum value: {value}")
