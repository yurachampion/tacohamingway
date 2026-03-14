# -*- coding: utf-8 -*-
"""
Добавляет lyrics_pl и lyrics_ru в data/content.json из data/genius_trjokat_warszawski.json.
Не трогает footnotes. Запустить один раз или после обновления genius JSON.
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CONTENT_PATH = BASE / "data" / "content.json"
GENIUS_PATH = BASE / "data" / "genius_trjokat_warszawski.json"

TRACK_SLUGS = {
    "Szlugi i kalafiory": "szlugi-i-kalafiory",
    "Marsz, marsz": "marsz-marsz",
    "Wszystko jedno": "wszystko-jedno",
    "Trójkąt": "trojkat",
    "(przerywnik)": "przerywnik",
    "Mięso": "mieso",
    "900729": "900729",
}
GENIUS_FOOTER = "[Tekst i adnotacje na Rap Genius Polska]"


def main():
    content = {"tracks": {}}
    if CONTENT_PATH.exists():
        content = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    if "tracks" not in content:
        content["tracks"] = {}

    if not GENIUS_PATH.exists():
        print("Файл не найден:", GENIUS_PATH)
        return

    genius = json.loads(GENIUS_PATH.read_text(encoding="utf-8"))
    for track in genius.get("tracks", []):
        title = track.get("title", "")
        slug = TRACK_SLUGS.get(title)
        if not slug:
            continue
        lyrics_pl = (track.get("lyrics_pl") or "").strip()
        if GENIUS_FOOTER in lyrics_pl:
            lyrics_pl = lyrics_pl.split(GENIUS_FOOTER)[0].strip()
        lyrics_ru = (track.get("lyrics_ru") or lyrics_pl).strip()
        if GENIUS_FOOTER in lyrics_ru:
            lyrics_ru = lyrics_ru.split(GENIUS_FOOTER)[0].strip()
        if slug not in content["tracks"]:
            content["tracks"][slug] = {"footnotes": {}}
        content["tracks"][slug]["lyrics_pl"] = lyrics_pl
        content["tracks"][slug]["lyrics_ru"] = lyrics_ru

    CONTENT_PATH.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Готово: lyrics_pl/lyrics_ru добавлены в content.json для всех треков.")


if __name__ == "__main__":
    main()
