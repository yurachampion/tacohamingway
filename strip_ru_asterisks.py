# -*- coding: utf-8 -*-
"""Удаляет из всех lyrics_ru в JSON вхождения *цифра (например *1, *2)."""
import json
import re
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "data" / "genius_trjokat_warszawski.json"


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    for track in data.get("tracks", []):
        if "lyrics_ru" in track and track["lyrics_ru"]:
            track["lyrics_ru"] = re.sub(r"\s*\*\d+", "", track["lyrics_ru"])
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Готово: звёздочки с цифрами убраны из всех lyrics_ru.")


if __name__ == "__main__":
    main()
