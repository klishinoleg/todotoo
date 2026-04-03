PYTHON ?= python
I18N_CLI ?= $(PYTHON) -m fastapi18n.utils.commands
LANGS ?= ru
LOCALE ?= locales
SOURCE_LANG ?= en

comma := ,
LANG_PIPE := $(subst $(comma),|,$(strip $(LANGS)))

.PHONY: localize i18n-makemessages translate help

i18n-makemessages: ## Extract messages and update locale catalogs
	$(I18N_CLI) -d "$(LOCALE)" -l "$(LANG_PIPE)" -s "$(SOURCE_LANG)" makemessages

translate: ## Auto-translate all .po files for LANGS (default: ru)
	$(PYTHON) translate.py --lang "$(LANGS)" --locale "$(LOCALE)"

localize: ## makemessages -> translate -> makemessages
	$(MAKE) i18n-makemessages LANGS="$(LANGS)" LOCALE="$(LOCALE)" SOURCE_LANG="$(SOURCE_LANG)"
	$(MAKE) translate LANGS="$(LANGS)" LOCALE="$(LOCALE)"
	$(MAKE) i18n-makemessages LANGS="$(LANGS)" LOCALE="$(LOCALE)" SOURCE_LANG="$(SOURCE_LANG)"

help:
	@echo "Usage:"
	@echo "  make localize LANGS=ru,de LOCALE=locales"
	@echo "  make i18n-makemessages LANGS=ru,de LOCALE=locales"
	@echo "  make translate LANGS=ru,de LOCALE=locales"
