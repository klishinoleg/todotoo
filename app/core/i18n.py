"""
Internationalization (i18n) setup for the application.

This module initializes the translation system using `fastapi18n`.
It configures:
- the directory where locale files are stored,
- the available languages,
- the default language for the application.

It also exposes convenient helpers:
    _           — gettext() alias, returns translated string,
    activate    — change active locale at runtime,
    get_lang    — get current active locale.

Usage example:

    from core.i18n import _
    welcome_text = _("Welcome to ToDoToo Club!")

    # Change language dynamically (e.g., in middleware)
    activate("fr")

    # Get current user language
    lang = get_lang()

Notes:
    - Locale files must be placed inside: `<project_root>/locales/<lang>/LC_MESSAGES/*.mo`
    - Languages list is controlled by environment variable `LANGUAGES`, parsed in settings.
"""

from fastapi18n.wrappers import TranslationWrapper
from core.config.settings import settings

# ----------------------------------------------------------------------
# Initialize translation system
# ----------------------------------------------------------------------
TranslationWrapper.init(
    locales_dir=settings.system.get_locales_dir(),
    languages=settings.system.get_languages(),
    language=settings.system.default_language,
)

# ----------------------------------------------------------------------
# Public translation helpers
# ----------------------------------------------------------------------

#: Alias for gettext translation function.
_ = TranslationWrapper.get_instance().gettext

#: Change active locale at runtime.
activate = TranslationWrapper.get_instance().set_locale

#: Retrieve current locale.
get_lang = TranslationWrapper.get_instance().get_locale
