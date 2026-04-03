from contextvars import ContextVar

from core.config.settings import settings

_current_lang: ContextVar[str] = ContextVar("todotoo_lang", default=settings.system.default_language)


def _(message: str) -> str:
    """
    Stub translator.
    Localization will be moved to explicit translation tables.
    """
    return message


def activate(language: str) -> None:
    _current_lang.set(language)


def get_lang() -> str:
    return _current_lang.get()

