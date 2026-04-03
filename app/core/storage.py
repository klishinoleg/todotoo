from functools import lru_cache

from core.di.storage import DIStorageProvider
from interfaces.storage.storage import Storage


@lru_cache(maxsize=1)
def get_storage() -> Storage:
    # Ensure provider side-effects are imported before DI resolution.
    import infrastructure.storage  # noqa: F401
    return DIStorageProvider.get()

