# -*- coding: utf-8 -*-
"""
Проверяет: у каждого выделенного слова (data-key) на страницах треков
есть ли сноска в referencesPl и referencesRu.
"""
import re
from pathlib import Path

TRACKS = [
    "szlugi-i-kalafiory",
    "marsz-marsz",
    "wszystko-jedno",
    "trojkat",
    "przerywnik",
    "mieso",
    "900729",
]


def main():
    base = Path(__file__).resolve().parent
    all_ok = True
    for slug in TRACKS:
        path = base / (slug + ".html")
        if not path.exists():
            print(f"  Пропуск: {path.name} не найден")
            continue
        html = path.read_text(encoding="utf-8")
        keys_in_html = set(int(m) for m in re.findall(r'data-key="(\d+)"', html))
        # Ключи в referencesPl/referencesRu в инлайн-скрипте: "  0: { title:" или "  12: { title:"
        keys_in_refs = set(int(m) for m in re.findall(r"^\s*(\d+)\s*:\s*\{\s*title\s*:", html, re.MULTILINE))
        missing = keys_in_html - keys_in_refs
        extra = keys_in_refs - keys_in_html
        if missing:
            print(f"{slug}: нет сносок для ключей: {sorted(missing)}")
            all_ok = False
        elif extra:
            print(f"{slug}: лишние сноски (нет выделения в тексте): {sorted(extra)}")
        else:
            print(f"{slug}: OK (ключей: {len(keys_in_html)})")
    if all_ok:
        print("\nУ всех выделенных слов есть сноски.")
    else:
        print("\nЕсть выделенные слова без сносок — см. выше.")


if __name__ == "__main__":
    main()
