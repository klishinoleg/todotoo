from __future__ import annotations

import importlib
import inspect
import pkgutil

from application.config.dto.enums import EnumItemDTO, EnumsConfigDTO
from core.enums import app as app_enums
from core.enums.base import BaseLabeledEnum
from core.i18n import get_lang, get_supported_languages


class ConfigEnumsUseCase:
    @staticmethod
    def _get_enum_classes() -> list[type[BaseLabeledEnum]]:
        classes: list[type[BaseLabeledEnum]] = []
        seen: set[type[BaseLabeledEnum]] = set()

        for module_info in pkgutil.walk_packages(app_enums.__path__, prefix=f"{app_enums.__name__}."):
            if module_info.ispkg:
                continue

            module = importlib.import_module(module_info.name)
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if not issubclass(obj, BaseLabeledEnum) or obj is BaseLabeledEnum:
                    continue
                if obj.__module__ != module.__name__:
                    continue
                if obj in seen:
                    continue

                seen.add(obj)
                classes.append(obj)

        classes.sort(key=lambda enum_cls: (enum_cls.__module__, enum_cls.__name__))
        return classes

    @staticmethod
    def _to_key(enum_cls: type[BaseLabeledEnum]) -> str:
        module = enum_cls.__module__.replace("core.enums.app.", "")
        return f"{module}.{enum_cls.__name__}"

    @staticmethod
    def _invalidate_enum_cache(enum_cls: type[BaseLabeledEnum]) -> None:
        for attr_name in ("_label_map", "choices"):
            attr = getattr(enum_cls, attr_name, None)
            clear_fn = getattr(attr, "cache_clear", None)
            if clear_fn:
                clear_fn()

    async def get_enums(self) -> EnumsConfigDTO:
        result: dict[str, list[EnumItemDTO]] = {}

        for enum_cls in self._get_enum_classes():
            self._invalidate_enum_cache(enum_cls)
            result[self._to_key(enum_cls)] = [
                EnumItemDTO(id=value, name=label)
                for value, label in enum_cls.choices()
            ]

        return EnumsConfigDTO(
            version="v1",
            language=get_lang(),
            supported_languages=list(get_supported_languages()),
            enums=result,
        )
