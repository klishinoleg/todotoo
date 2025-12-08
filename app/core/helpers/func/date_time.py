from datetime import datetime, timezone
from core.config.settings import settings
import zoneinfo


def get_utc_time() -> datetime:
    """
    Return the current UTC time as a timezone-aware `datetime` object.

    This helper ensures consistent usage of UTC across the application,
    avoiding local timezone issues and keeping all timestamps normalized.

    Returns:
        datetime: Current time in UTC with `tz=timezone.utc`.
    """
    return datetime.now(tz=timezone.utc)


def get_local_time(
        utc_datetime: datetime | None = None, tz: str = settings.system.default_timezone
) -> tuple[datetime, str]:
    """
    Convert a UTC datetime into a specified timezone or return the current
    time in that timezone if no datetime is provided.

    Args:
        utc_datetime (datetime | None):
            A timezone-aware UTC datetime.
            If None, returns the current datetime in the given timezone.
        tz (str):
            Timezone identifier in IANA format (e.g., "Europe/Moscow",
            "Asia/Shanghai", "America/New_York").

    Returns:
        Tuple:
            datetime:
                Timezone-aware datetime converted to the specified timezone.
            str: Timezone Name

    Raises:
        tz.ZoneInfoNotFoundError:
            If the provided timezone string is invalid or unknown.

    Notes:
        - If utc_datetime is provided but is naive (no tzinfo),
          it will be treated as UTC by default.
        - Uses Python's built-in `zone info` module (PEP 615).
    """
    tz_info = zoneinfo.ZoneInfo(key=tz)

    if utc_datetime is None:
        # If no datetime is provided — return current time in tz
        return datetime.now(tz=tz_info), str(tz_info)

    # If datetime is naive — assume UTC explicitly
    if utc_datetime.tzinfo is None:
        utc_datetime = utc_datetime.replace(tzinfo=timezone.utc)

    # Convert from UTC to the desired timezone
    return utc_datetime.astimezone(tz_info), str(tz_info)
