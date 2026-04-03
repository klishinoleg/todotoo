from __future__ import annotations

import gettext
from contextvars import ContextVar
from functools import lru_cache

from core.config.settings import settings


def _build_supported_languages() -> tuple[str, ...]:
    languages = tuple(code for code, _ in settings.system.get_languages())
    return languages if languages else ("en",)


_SUPPORTED_LANGUAGES = _build_supported_languages()


def _normalize_lang(value: str | None) -> str:
    if value is None:
        return ""
    return value.strip().lower().replace("_", "-")


def _match_supported_language(value: str | None) -> str | None:
    normalized = _normalize_lang(value)
    if not normalized:
        return None

    candidates = [normalized]
    if "-" in normalized:
        candidates.append(normalized.split("-", 1)[0])

    for candidate in candidates:
        if candidate in _SUPPORTED_LANGUAGES:
            return candidate
    return None


_DEFAULT_LANGUAGE = _match_supported_language(settings.system.default_language) or _SUPPORTED_LANGUAGES[0]
_current_lang: ContextVar[str] = ContextVar("todotoo_lang", default=_DEFAULT_LANGUAGE)


def get_supported_languages() -> tuple[str, ...]:
    return _SUPPORTED_LANGUAGES


def get_locales_dir() -> Path:
    return settings.system.get_locales_dir()


@lru_cache(maxsize=64)
def _get_translator(language: str) -> gettext.NullTranslations:
    return gettext.translation(
        "messages",
        localedir=str(get_locales_dir()),
        languages=[language],
        fallback=True,
    )


def reload_translations() -> None:
    _get_translator.cache_clear()


def resolve_language(language: str | None = None, accept_language: str | None = None) -> str:
    selected = _match_supported_language(language)
    if selected:
        return selected

    if accept_language:
        for entry in accept_language.split(","):
            token = entry.split(";", 1)[0].strip()
            selected = _match_supported_language(token)
            if selected:
                return selected

    return _DEFAULT_LANGUAGE


def activate(language: str | None = None, accept_language: str | None = None) -> str:
    selected = resolve_language(language=language, accept_language=accept_language)
    _current_lang.set(selected)
    return selected


def reset() -> None:
    _current_lang.set(_DEFAULT_LANGUAGE)


def get_lang() -> str:
    return resolve_language(language=_current_lang.get())


def _(message: str) -> str:
    return _get_translator(get_lang()).gettext(message)


def ngettext(singular: str, plural: str, number: int) -> str:
    return _get_translator(get_lang()).ngettext(singular, plural, number)
