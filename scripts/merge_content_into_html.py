# -*- coding: utf-8 -*-
"""
Читает data/content.json и подставляет сноски в HTML треков.
- Ключи нумеруются автоматически по порядку фразы в тексте (0 = первая фраза, 1 = вторая, ...).
- Выделения: в польской колонке по fragment_pl, в русской по fragment_ru (если не заполнен — выделения нет).
- Если заголовок и текст сноски пусты — при клике ничего не показывается.
Запускать после правок в админке.
"""
import html as html_module
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


def normalize_whitespace(s):
    return " ".join((s or "").split())


def build_line_html(line_text, regions_for_line):
    """Собирает HTML одной строки: оборачивает фрагменты в <span class="keyword" data-key="k">."""
    regions_for_line = sorted(regions_for_line, key=lambda r: r[0])
    parts = []
    pos = 0
    for start, end, key in regions_for_line:
        if start > pos:
            parts.append(html_module.escape(line_text[pos:start]))
        parts.append('<span class="keyword" data-key="%d">%s</span>' % (key, html_module.escape(line_text[start:end])))
        pos = end
    if pos < len(line_text):
        parts.append(html_module.escape(line_text[pos:]))
    return "".join(parts)


def section_label(line):
    s = (line or "").strip()
    return s.startswith("[") and s.endswith("]")


def find_fragment_position_in_lines(lines, fragment):
    """Ищет первое вхождение fragment в lines. Возвращает (line_idx, start, end) или None."""
    frag = normalize_whitespace(fragment).strip()
    if not frag:
        return None
    full = "\n".join(lines)
    full_norm = normalize_whitespace(full)
    frag_norm = normalize_whitespace(frag)
    if frag_norm not in full_norm:
        return None
    # Позиция в full_norm
    idx = full_norm.find(frag_norm)
    if idx < 0:
        return None
    # Сопоставляем с линиями: считаем символы до idx
    pos = 0
    for line_idx, line in enumerate(lines):
        line_norm = normalize_whitespace(line)
        line_len = len(line_norm) + (1 if line_idx < len(lines) - 1 else 0)  # +1 за \n
        if pos + len(line_norm) > idx:
            start_in_line = idx - pos
            end_in_line = min(start_in_line + len(frag_norm), len(line_norm))
            return (line_idx, start_in_line, end_in_line)
        pos += line_len + 1
    return None


def find_fragment_region_in_line(line_text, fragment):
    """Ищет fragment в одной строке line_text. Возвращает (start, end) или None."""
    frag = (fragment or "").strip()
    if not frag or frag not in line_text:
        return None
    start = line_text.find(frag)
    return (start, start + len(frag))


def position_to_line_offset(lines, pos):
    """По позиции pos в полном тексте (lines, join \\n) возвращает (line_idx, start_in_line, end_in_line) для конца фрагмента длиной 0 (точка)."""
    current = 0
    for line_idx, line in enumerate(lines):
        line_len = len(line) + (1 if line_idx < len(lines) - 1 else 0)
        if current + len(line) > pos:
            start_in_line = pos - current
            return (line_idx, start_in_line)
        current += line_len
    return (len(lines) - 1, 0)


def find_fragment_in_lines(lines, fragment):
    """Ищет fragment в lines. Возвращает (line_idx, start, end) или None. Сначала точное совпадение, потом по строке с нормализацией пробелов."""
    frag = (fragment or "").strip()
    if not frag:
        return None
    full = "\n".join(lines)
    if frag in full:
        pos = full.find(frag)
        current = 0
        for line_idx, line in enumerate(lines):
            end = current + len(line)
            if pos < end:
                start_in_line = pos - current
                return (line_idx, start_in_line, start_in_line + len(frag))
            current = end + 1
        return None
    frag_norm = normalize_whitespace(frag)
    for line_idx, line in enumerate(lines):
        line_norm = normalize_whitespace(line)
        if frag_norm not in line_norm:
            continue
        start_norm = line_norm.find(frag_norm)
        if start_norm < 0:
            continue
        start, end = _norm_pos_to_line_pos(line, line_norm, start_norm, len(frag_norm))
        return (line_idx, start, end)
    return None


def _norm_pos_to_line_pos(line, line_norm, start_norm, length_norm):
    """Отображает срез line_norm[start_norm:start_norm+length_norm] на позиции в line (по счётчику непробельных символов)."""
    n = 0
    start_orig = 0
    for i, c in enumerate(line):
        if c in " \t\n":
            continue
        if n == start_norm:
            start_orig = i
        if n == start_norm + length_norm:
            return (start_orig, i)
        n += 1
    return (start_orig, len(line))


def sorted_footnotes_by_position(footnotes, lines, fragment_key="fragment_pl"):
    """
    Возвращает список (new_key, footnote) отсортированный по положению fragment в тексте.
    new_key = 1, 2, 3, ... (нумерация с 1).
    """
    items = []
    for k, fn in (footnotes or {}).items():
        frag = (fn.get(fragment_key) or "").strip()
        if not frag:
            continue
        loc = find_fragment_in_lines(lines, frag)
        if loc is not None:
            line_idx, start, end = loc
            items.append((line_idx, start, fn))
    items.sort(key=lambda x: (x[0], x[1]))
    return [(i + 1, fn) for i, (_, _, fn) in enumerate(items)]


def regions_by_line(lines, sorted_list, fragment_key):
    """sorted_list = [(key, footnote), ...]. Ищем fragment в lines через find_fragment_in_lines; by_line[line_idx] = [(start, end, key), ...]."""
    by_line = {}
    for key, fn in sorted_list:
        frag = (fn.get(fragment_key) or "").strip()
        if not frag:
            continue
        loc = find_fragment_in_lines(lines, frag)
        if loc is None:
            continue
        line_idx, start, end = loc
        by_line.setdefault(line_idx, []).append((start, end, key))
    for line_idx in by_line:
        seen = set()
        out = []
        for r in sorted(by_line[line_idx], key=lambda x: (x[0], x[1])):
            t = (r[0], r[1])
            if t not in seen:
                seen.add(t)
                out.append(r)
        by_line[line_idx] = out
    return by_line


def build_lyrics_block_from_content(lines_pl, lines_ru, by_line_pl, by_line_ru):
    """Собирает HTML блока лирики: lyrics-part и lyrics-line-pair."""
    out = []
    in_part = False
    n = len(lines_pl)
    for i in range(n):
        line_pl = lines_pl[i]
        line_ru = lines_ru[i] if i < len(lines_ru) else ""
        is_section = section_label(line_pl)
        if is_section and in_part:
            out.append("</div>")
            in_part = False
        if is_section or not in_part:
            out.append('<div class="lyrics-part">')
            in_part = True
        regs_pl = by_line_pl.get(i, [])
        regs_ru = by_line_ru.get(i, [])
        pl_inner = build_line_html(line_pl, regs_pl)
        ru_inner = build_line_html(line_ru, regs_ru)
        if is_section:
            pl_inner = "<em>%s</em>" % pl_inner
            if (line_ru or "").strip().startswith("["):
                ru_inner = "<em>%s</em>" % ru_inner
        out.append(
            '<div class="lyrics-line-pair">'
            '<div class="lyrics-line-pl"><p>%s</p></div>'
            '<div class="lyrics-line-ru"><p>%s</p></div>'
            "</div>" % (pl_inner, ru_inner)
        )
    if in_part:
        out.append("</div>")
    return "\n".join(out)


def get_existing_data_keys(html):
    """Возвращает отсортированный список уникальных ключей data-key из HTML (чтобы при fallback refs совпадали со span)."""
    keys = set()
    for m in re.finditer(r'data-key="(\d+)"', html):
        keys.add(int(m.group(1)))
    return sorted(keys)


def get_lyrics_block_bounds(html):
    """Возвращает (lyrics_start, lyrics_end) для div#lyricsPolish."""
    lyrics_start = html.find('id="lyricsPolish">')
    if lyrics_start == -1:
        return None, None
    lyrics_start += len('id="lyricsPolish">')
    pos = lyrics_start
    depth = 1
    lyrics_end = None
    while pos < len(html):
        next_close = html.find("</div>", pos)
        next_open = html.find("<div", pos)
        if next_close == -1:
            break
        use_close = next_open == -1 or next_close < next_open
        if use_close:
            depth -= 1
            pos = next_close + 6
            if depth == 0:
                lyrics_end = next_close
                break
        else:
            if next_open + 5 <= len(html) and html[next_open : next_open + 5] != "</div":
                depth += 1
            pos = html.find(">", next_open) + 1 if html.find(">", next_open) != -1 else next_open + 5
    return lyrics_start, lyrics_end


def youtube_id(url):
    if not url or not isinstance(url, str):
        return None
    url = url.strip()
    m = re.search(r"[?&]v=([a-zA-Z0-9_-]{11})", url)
    if m:
        return m.group(1)
    m = re.search(r"youtu\.be/([a-zA-Z0-9_-]{11})", url)
    if m:
        return m.group(1)
    return None


def refs_pl_from_sorted(sorted_list):
    """Строит только referencesPl из списка (key, footnote) — только поля для польского."""
    refs = {}
    for key, fn in sorted_list:
        vid = youtube_id(fn.get("video"))
        refs[key] = {
            "title": (fn.get("title_pl") or "").strip(),
            "text": (fn.get("text_pl") or "").strip(),
            "url": (fn.get("url") or "").strip(),
        }
        if fn.get("image"):
            refs[key]["image"] = fn.get("image")
        if vid:
            refs[key]["videoId"] = vid
    return refs


def refs_ru_from_sorted(sorted_list):
    """Строит только referencesRu из списка (key, footnote) — только поля для русского."""
    refs = {}
    for key, fn in sorted_list:
        vid = youtube_id(fn.get("video"))
        refs[key] = {
            "title": (fn.get("title_ru") or "").strip(),
            "text": (fn.get("text_ru") or "").strip(),
            "url": (fn.get("url") or "").strip(),
        }
        if fn.get("image"):
            refs[key]["image"] = fn.get("image")
        if vid:
            refs[key]["videoId"] = vid
    return refs


def refs_to_js(refs_pl, refs_ru):
    def entry(k, v):
        parts = [
            "title: %s" % json.dumps(v.get("title", ""), ensure_ascii=False),
            "text: %s" % json.dumps(v.get("text", ""), ensure_ascii=False),
            "url: %s" % json.dumps(v.get("url", ""), ensure_ascii=False),
        ]
        if v.get("image"):
            parts.append("image: %s" % json.dumps(v["image"], ensure_ascii=False))
        if v.get("videoId"):
            parts.append("videoId: %s" % json.dumps(v["videoId"], ensure_ascii=False))
        return "%s: { %s }" % (k, ", ".join(parts))
    pl_str = "{\n  " + ",\n  ".join(entry(k, refs_pl[k]) for k in sorted(refs_pl.keys(), key=int)) + "\n}"
    ru_str = "{\n  " + ",\n  ".join(entry(k, refs_ru[k]) for k in sorted(refs_ru.keys(), key=int)) + "\n}"
    return "var referencesPl = %s;\nvar referencesRu = %s;" % (pl_str, ru_str)


def main():
    if not CONTENT_PATH.exists():
        print("Файл не найден:", CONTENT_PATH)
        return
    data = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    tracks_data = data.get("tracks") or {}
    for slug in TRACKS:
        html_path = BASE / (slug + ".html")
        if not html_path.exists():
            print("Пропуск (нет HTML):", slug)
            continue
        html = html_path.read_text(encoding="utf-8")
        track_data = tracks_data.get(slug) or {}
        footnotes = track_data.get("footnotes") or {}
        lyrics_pl = (track_data.get("lyrics_pl") or "").strip()
        lyrics_ru = (track_data.get("lyrics_ru") or lyrics_pl).strip()
        lines_pl = [ln for ln in lyrics_pl.split("\n")]
        lines_ru = [ln for ln in lyrics_ru.split("\n")]

        sorted_list_pl = sorted_footnotes_by_position(footnotes, lines_pl, "fragment_pl")
        sorted_list_ru = sorted_footnotes_by_position(footnotes, lines_ru, "fragment_ru")
        if sorted_list_pl or sorted_list_ru:
            by_line_pl = regions_by_line(lines_pl, sorted_list_pl, "fragment_pl")
            by_line_ru = regions_by_line(lines_ru, sorted_list_ru, "fragment_ru")
            new_lyrics_block = build_lyrics_block_from_content(lines_pl, lines_ru, by_line_pl, by_line_ru)
            refs_pl = refs_pl_from_sorted(sorted_list_pl)
            refs_ru = refs_ru_from_sorted(sorted_list_ru)
            refs_js = refs_to_js(refs_pl, refs_ru)
            lyrics_start, lyrics_end = get_lyrics_block_bounds(html)
            if lyrics_start is not None and lyrics_end is not None:
                html = html[:lyrics_start] + new_lyrics_block + html[lyrics_end:]
        else:
            keys_sorted = sorted((k for k in (footnotes or {}) if str(k).isdigit()), key=lambda x: int(x))
            existing_keys = get_existing_data_keys(html)
            if not existing_keys:
                existing_keys = [i + 1 for i in range(len(keys_sorted))]
            sorted_fallback = [(existing_keys[i], footnotes[k]) for i, k in enumerate(keys_sorted) if i < len(existing_keys)]
            refs_pl = refs_pl_from_sorted(sorted_fallback)
            refs_ru = refs_ru_from_sorted(sorted_fallback)
            refs_js = refs_to_js(refs_pl, refs_ru)

        TRACK_JS_TAG = '<script src="track.js"></script>'
        new_scripts = "  <script>\n" + refs_js + "\n  </script>\n  " + TRACK_JS_TAG
        track_js_pos = html.rfind(TRACK_JS_TAG)
        if track_js_pos >= 0:
            # Find the opening <script> tag that immediately precedes track.js include
            before = html[:track_js_pos].rstrip('\r\n ')
            if before.endswith('</script>'):
                # Find its opening <script> tag
                open_tag_pos = html.rfind('<script>', 0, track_js_pos)
                if open_tag_pos >= 0:
                    html = html[:open_tag_pos] + new_scripts + html[track_js_pos + len(TRACK_JS_TAG):]
                else:
                    html = html[:track_js_pos] + new_scripts[html.rfind('\n', 0, track_js_pos) + 1:] + html[track_js_pos + len(TRACK_JS_TAG):]
            else:
                # No inline script before track.js — just insert new one before it
                html = html[:track_js_pos] + "  <script>\n" + refs_js + "\n  </script>\n  " + html[track_js_pos:]

        note_pl = (track_data.get("note_pl") or "").strip()
        note_ru = (track_data.get("note_ru") or "").strip()
        title_pl = (track_data.get("title_pl") or "").strip()
        title_ru = (track_data.get("title_ru") or "").strip()
        note_pl_esc = html_module.escape(note_pl)
        note_ru_esc = html_module.escape(note_ru)
        if "notes-block" in html:
            if note_pl or note_ru:
                notes_pattern = re.compile(
                    r'(<div class="note-block note-pl">.*?<blockquote class="lyrics-note">).*?'
                    r'(</blockquote>.*?<div class="note-block note-ru">.*?<blockquote class="lyrics-note">).*?'
                    r'(</blockquote>)',
                    re.DOTALL,
                )
                _npl = note_pl_esc
                _nru = note_ru_esc
                html = notes_pattern.sub(
                    lambda m: m.group(1) + _npl + m.group(2) + _nru + m.group(3),
                    html,
                    count=1,
                )
        elif '<div class="lyrics-columns' in html:
            notes_block = (
                '\n        <div class="notes-block">\n'
                '          <div class="note-block note-pl">\n'
                '            <h4 class="note-label">Примечание (польский)</h4>\n'
                '            <blockquote class="lyrics-note">' + note_pl_esc + '</blockquote>\n'
                '          </div>\n'
                '          <div class="note-block note-ru">\n'
                '            <h4 class="note-label">Примечание (русский)</h4>\n'
                '            <blockquote class="lyrics-note">' + note_ru_esc + '</blockquote>\n'
                '          </div>\n'
                '        </div>\n        '
            )
            html = html.replace(
                '<div class="lyrics-columns',
                notes_block + '<div class="lyrics-columns',
                1,
            )
        if title_pl or title_ru:
            h1_text = title_pl or title_ru
            h1_content = html_module.escape(h1_text)
            if title_pl and title_ru:
                subtitle = html_module.escape(title_ru)
                new_title_block = '<h1 class="track-page-title">' + h1_content + '</h1>\n    <p class="track-subtitle">' + subtitle + "</p>"
            else:
                new_title_block = '<h1 class="track-page-title">' + h1_content + "</h1>"
            html = re.sub(r"<h1 class=\"track-page-title\">.*?</h1>(\s*<p class=\"track-subtitle\">.*?</p>)?", new_title_block, html, count=1, flags=re.DOTALL)
            page_title = (title_ru or title_pl or "").strip()
            if page_title:
                html = re.sub(r"<title>.*?</title>", "<title>" + html_module.escape(page_title) + " — Разбор треков</title>", html, count=1)
        html_path.write_text(html, encoding="utf-8")
        print("OK:", slug)
    print("Готово. Сноски из content.json подставлены в HTML (ключи по порядку в тексте).")


if __name__ == "__main__":
    main()
