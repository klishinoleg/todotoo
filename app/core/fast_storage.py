from functools import lru_cache

from core.di.fast_storage import DIFastStorageProvider
from interfaces.fast_storage.fast_storage import FastStorage


@lru_cache(maxsize=1)
def get_fast_storage() -> FastStorage:
    import infrastructure.fast_storage  # noqa: F401

    return DIFastStorageProvider.get()
