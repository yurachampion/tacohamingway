# -*- coding: utf-8 -*-
"""
Заполняет fragment_pl в data/content.json из текущего HTML: для каждого ключа
берётся текст внутри <span class="keyword" data-key="N"> в польской колонке.
Запустить один раз после extract_content_from_html.
"""
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CONTENT_PATH = BASE / "data" / "content.json"
TRACKS = [
    "szlugi-i-kalafiory",
    "marsz-marsz",
    "wszystko-jedno",
    "trojkat",
    "przerywnik",
    "mieso",
    "900729",
]


def extract_fragments_from_html(html):
    """Находит все <span class="keyword" data-key="N">...</span> в .lyrics-line-pl, возвращает dict key -> inner_text."""
    fragments = {}
    # Ищем в блоке lyricsPolish
    pattern = re.compile(
        r'<span\s+class="keyword"\s+data-key="(\d+)">(.*?)</span>',
        re.DOTALL,
    )
    for m in pattern.finditer(html):
        key = m.group(1)
        inner = m.group(2)
        inner = re.sub(r"<[^>]+>", "", inner)  # убрать вложенные теги
        inner = inner.replace("&nbsp;", " ").strip()
        if key not in fragments:
            fragments[key] = inner
    return fragments


def main():
    if not CONTENT_PATH.exists():
        print("Файл не найден:", CONTENT_PATH)
        return
    content = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    for slug in TRACKS:
        path = BASE / (slug + ".html")
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        frags = extract_fragments_from_html(html)
        if slug not in content.get("tracks", {}):
            continue
        footnotes = content["tracks"][slug].get("footnotes") or {}
        for key, text in frags.items():
            if key in footnotes:
                footnotes[key]["fragment_pl"] = text
    CONTENT_PATH.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Готово: fragment_pl заполнен из HTML для всех треков.")


if __name__ == "__main__":
    main()
