import json
import os
from pathlib import Path

import lyricsgenius
import requests


ARTIST = "Taco Hemingway"
ALBUM_NAME = "Trójkąt Warszawski"

# Жёстко задаём треклист, как на сайте
TRACKS = [
    "Szlugi i kalafiory",
    "Marsz, marsz",
    "Wszystko jedno",
    "Trójkąt",
    "(przerywnik)",
    "Mięso",
    "900729",
]


def get_genius_client() -> lyricsgenius.Genius:
    token = os.getenv("GENIUS_ACCESS_TOKEN")
    if not token:
        raise RuntimeError(
            "ENV-переменная GENIUS_ACCESS_TOKEN не задана. "
            "Создай токен на Genius и экспортируй его, например:\n"
            "  set GENIUS_ACCESS_TOKEN=...   (Windows PowerShell/cmd)\n"
        )
    genius = lyricsgenius.Genius(
        token,
        timeout=15,
        retries=3,
        skip_non_songs=True,
        excluded_terms=["(Live)", "(Remix)", "(Remastered)"],
    )
    genius.verbose = False
    return genius


def fetch_annotations(song_id: int, token: str):
    """Тянем аннотации через официальный /referents API Genius.
    Здесь только собираем данные, но НИЧЕГО не форматируем под HTML.
    """
    url = "https://api.genius.com/referents"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"song_id": song_id, "per_page": 50}

    out = []
    page = 1
    while True:
        params["page"] = page
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json().get("response", {})
        referents = data.get("referents", [])
        for ref in referents:
            fragment = ref.get("fragment") or ""
            for ann in ref.get("annotations", []):
                body = (
                    ann.get("body", {}).get("plain")
                    or ann.get("body", {}).get("dom", {}).get("children")
                )
                out.append(
                    {
                        "fragment": fragment,
                        "annotation": body,
                        "url": ann.get("url"),
                    }
                )
        if not data.get("next_page"):
            break
        page = data["next_page"]
    return out


def translate_placeholder(text: str, target_lang: str = "ru") -> str:
    """Заглушка для перевода.

    СЮДА можно воткнуть любой API‑переводчик (DeepL, Яндекс, OpenAI и т.п.).
    Сейчас просто возвращает исходный текст, чтобы не нарушать авторские права.
    """
    return text


def get_song_id(song) -> int | None:
    """Аккуратно достаём ID трека из разных версий lyricsgenius."""
    # Новые версии: атрибут id
    if hasattr(song, "id"):
        return song.id
    # Иногда есть song_id
    if hasattr(song, "song_id"):
        return song.song_id
    # to_dict() → { "id": ... }
    to_dict = getattr(song, "to_dict", None)
    if callable(to_dict):
        data = to_dict()
        if isinstance(data, dict) and "id" in data:
            return data["id"]
    # В крайнем случае пробуем внутренний _body
    body = getattr(song, "_body", None)
    if isinstance(body, dict) and "id" in body:
        return body["id"]
    return None


def main():
    base_dir = Path(__file__).resolve().parent
    out_dir = base_dir / "data"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "genius_trjokat_warszawski.json"

    genius = get_genius_client()
    token = os.environ["GENIUS_ACCESS_TOKEN"]

    album_data = {
        "artist": ARTIST,
        "album": ALBUM_NAME,
        "tracks": [],
    }

    for title in TRACKS:
        print(f"Ищу трек: {title!r}...")
        song = genius.search_song(title, ARTIST)
        if not song:
            print(f"  ⚠ Не нашёл на Genius: {title}")
            continue

        song_id = get_song_id(song)
        if not song_id:
            print(f"  ⚠ Нашёл песню '{song.title}', но не смог узнать её ID, пропускаю аннотации.")
        else:
            print(f"  ✓ Нашёл: {song.title} (id={song_id})")

        lyrics_original = song.lyrics or ""
        lyrics_ru = translate_placeholder(lyrics_original, target_lang="ru")

        annotations = fetch_annotations(song_id, token) if song_id else []

        album_data["tracks"].append(
            {
                "title": title,
                "genius_title": song.title,
                "genius_url": song.url,
                "song_id": song_id,
                "lyrics_pl": lyrics_original,
                "lyrics_ru": lyrics_ru,
                "annotations": annotations,
            }
        )

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(album_data, f, ensure_ascii=False, indent=2)

    print(f"\nГотово. Данные сохранены в {out_path}")


if __name__ == "__main__":
    main()

