from __future__ import annotations

import argparse
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

import polib  # type: ignore[import-untyped]


TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"


def translate_text(text: str, target_lang: str) -> str:
    if not text.strip():
        return text

    query = urllib.parse.urlencode(
        {
            "client": "gtx",
            "sl": "auto",
            "tl": target_lang,
            "dt": "t",
            "q": text,
        }
    )
    request = urllib.request.Request(
        f"{TRANSLATE_URL}?{query}",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))

    chunks = payload[0] if payload and isinstance(payload, list) else []
    translated = "".join(chunk[0] for chunk in chunks if chunk and len(chunk) > 0 and isinstance(chunk[0], str))
    return translated or text


def process_po_file(po_path: Path, target_lang: str, delay: float) -> tuple[int, int]:
    po = polib.pofile(str(po_path), encoding="utf-8")
    translated_count = 0
    skipped_count = 0
    cache: dict[str, str] = {}

    for entry in po:
        if entry.obsolete or not entry.msgid:
            skipped_count += 1
            continue

        try:
            if entry.msgid_plural:
                for index, source_text in ((0, entry.msgid), (1, entry.msgid_plural)):
                    current_value = entry.msgstr_plural.get(index, "").strip()
                    if current_value:
                        skipped_count += 1
                        continue

                    if source_text not in cache:
                        cache[source_text] = translate_text(source_text, target_lang)
                        time.sleep(delay)
                    entry.msgstr_plural[index] = cache[source_text]
                    translated_count += 1
            else:
                if entry.msgstr.strip():
                    skipped_count += 1
                    continue
                if entry.msgid not in cache:
                    cache[entry.msgid] = translate_text(entry.msgid, target_lang)
                    time.sleep(delay)
                entry.msgstr = cache[entry.msgid]
                translated_count += 1
        except Exception:
            if entry.msgid_plural:
                entry.msgstr_plural[0] = entry.msgstr_plural.get(0) or entry.msgid
                entry.msgstr_plural[1] = entry.msgstr_plural.get(1) or entry.msgid_plural
            else:
                entry.msgstr = entry.msgstr or entry.msgid

    po.save(str(po_path))
    return translated_count, skipped_count


def parse_languages(raw_langs: str) -> list[str]:
    values = [item.strip().lower() for item in re.split(r"[,\|]", raw_langs) if item.strip()]
    return values or ["ru"]


def resolve_locale_root(raw_locale: str) -> Path:
    locale_root = Path(raw_locale)
    if not locale_root.is_absolute():
        locale_root = Path(__file__).resolve().parent / locale_root
    return locale_root.resolve()


def main() -> None:
    parser = argparse.ArgumentParser(description="Translate locale .po files.")
    parser.add_argument("--lang", default="ru", help="Target language(s), e.g. ru or ru,de")
    parser.add_argument("--locale", default="locales", help="Locale directory under app/, e.g. locales or other")
    parser.add_argument("--delay", type=float, default=0.05, help="Delay between external translation calls")
    parser.add_argument("--locale-dir", dest="locale", help=argparse.SUPPRESS)
    args = parser.parse_args()

    locale_root = resolve_locale_root(args.locale)
    languages = parse_languages(args.lang)

    total_translated = 0
    total_skipped = 0
    processed_files = 0

    for target_lang in languages:
        target_root = locale_root / target_lang / "LC_MESSAGES"
        po_files = sorted(target_root.glob("*.po"))
        if not po_files:
            print(f"No .po files found in {target_root}")
            continue

        for po_file in po_files:
            translated, skipped = process_po_file(po_file, target_lang, args.delay)
            total_translated += translated
            total_skipped += skipped
            processed_files += 1
            print(f"{po_file}: translated={translated}, skipped={skipped}")

    if processed_files == 0:
        raise SystemExit(f"No .po files found in {locale_root}")

    print(
        "Done. "
        f"languages={','.join(languages)} "
        f"files={processed_files} "
        f"translated={total_translated}, skipped={total_skipped}"
    )


if __name__ == "__main__":
    main()
