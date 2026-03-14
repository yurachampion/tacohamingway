# -*- coding: utf-8 -*-
"""
Читает data/genius_trjokat_warszawski.json и генерирует:
- HTML блок текста (польский + сноски по аннотациям Genius)
- JS с referencesPl и referencesRu для каждой страницы трека.
Обновляет все HTML-страницы треков и подключает track.js с инлайн-данными сносок.
"""
import json
import re
import html
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "genius_trjokat_warszawski.json"
GENIUS_FOOTER = "[Tekst i adnotacje na Rap Genius Polska]"

TRACK_SLUGS = {
    "Szlugi i kalafiory": "szlugi-i-kalafiory",
    "Marsz, marsz": "marsz-marsz",
    "Wszystko jedno": "wszystko-jedno",
    "Trójkąt": "trojkat",
    "(przerywnik)": "przerywnik",
    "Mięso": "mieso",
    "900729": "900729",
}


def annotation_to_plain(node):
    """Рекурсивно извлекает plain text из узла аннотации (tag/children)."""
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, list):
        return "".join(annotation_to_plain(c) for c in node)
    if isinstance(node, dict):
        tag = node.get("tag", "")
        children = node.get("children", [])
        text = annotation_to_plain(children)
        if tag == "br":
            return "\n"
        if tag == "hr":
            return "\n—\n"
        if tag == "blockquote":
            return "\n" + text.strip() + "\n"
        if tag == "p":
            return "\n" + text.strip() + "\n"
        return text
    return ""


def normalize_whitespace(s):
    return re.sub(r"\s+", " ", (s or "").strip())


def find_fragment_regions(lyrics_lines, annotations):
    """
    Для каждого фрагмента аннотации ищем его в тексте (нормализуя пробелы)
    и возвращаем список регионов: (line_idx, start, end, key).
    """
    # Строим нормализованную строку с привязкой к (line_idx, offset)
    normalized = []
    for line_idx, line in enumerate(lyrics_lines):
        for offset, c in enumerate(line):
            if c.isspace() or c == "\n":
                if normalized and normalized[-1][0] != " ":
                    normalized.append((" ", line_idx, offset))
            else:
                normalized.append((c, line_idx, offset))
    norm_str = "".join(n[0] for n in normalized)

    regions = []
    for key, ann in enumerate(annotations):
        fragment = (ann.get("fragment") or "").strip()
        frag_norm = normalize_whitespace(fragment)
        if not frag_norm:
            continue
        # Только первое вхождение фрагмента, чтобы не дублировать текст
        start_norm = norm_str.find(frag_norm)
        if start_norm == -1:
            continue
        end_norm = start_norm + len(frag_norm)
        if end_norm > len(normalized):
            continue
        (_, line_idx0, off0) = normalized[start_norm]
        (_, line_idx1, off1) = normalized[end_norm - 1]
        if line_idx0 == line_idx1:
            regions.append((line_idx0, off0, off1 + 1, key))
        else:
            regions.append((line_idx0, off0, len(lyrics_lines[line_idx0]), key))
            for li in range(line_idx0 + 1, line_idx1):
                regions.append((li, 0, len(lyrics_lines[li]), key))
            regions.append((line_idx1, 0, off1 + 1, key))

    return regions


def build_line_html(line_text, regions_for_line, escape=True):
    """Собирает HTML одной строки: оборачивает фрагменты в <span class="keyword" data-key="k">."""
    if escape:
        def esc(s):
            return html.escape(s)
    else:
        def esc(s):
            return s

    regions_for_line = sorted(regions_for_line, key=lambda r: r[0])
    parts = []
    pos = 0
    for start, end, key in regions_for_line:
        if start > pos:
            parts.append(esc(line_text[pos:start]))
        parts.append('<span class="keyword" data-key="%d">%s</span>' % (key, esc(line_text[start:end])))
        pos = end
    if pos < len(line_text):
        parts.append(esc(line_text[pos:]))
    return "".join(parts)


def section_label(line):
    """Проверяет, является ли строка заголовком секции [Intro], [Refren] и т.д."""
    s = line.strip()
    return s.startswith("[") and s.endswith("]")


def build_track_data(track):
    """По данным трека из JSON строит lyrics_lines с регионами, referencesPl, referencesRu."""
    lyrics_pl = (track.get("lyrics_pl") or "").strip()
    if GENIUS_FOOTER in lyrics_pl:
        lyrics_pl = lyrics_pl.split(GENIUS_FOOTER)[0].strip()
    lyrics_ru = (track.get("lyrics_ru") or lyrics_pl).strip()
    if GENIUS_FOOTER in lyrics_ru:
        lyrics_ru = lyrics_ru.split(GENIUS_FOOTER)[0].strip()

    lines_pl = [ln for ln in lyrics_pl.split("\n")]
    lines_ru = [ln for ln in lyrics_ru.split("\n")]
    annotations = track.get("annotations") or []

    regions = find_fragment_regions(lines_pl, annotations)
    by_line = {}
    for (line_idx, start, end, key) in regions:
        by_line.setdefault(line_idx, []).append((start, end, key))
    # Убираем дубли: один и тот же (start, end) на строке — оставляем только первый key
    for line_idx in by_line:
        seen = set()
        out = []
        for (start, end, key) in sorted(by_line[line_idx], key=lambda x: (x[0], x[1], x[2])):
            t = (start, end)
            if t not in seen:
                seen.add(t)
                out.append((start, end, key))
        by_line[line_idx] = out

    refs_pl = {}
    refs_ru = {}
    for key, ann in enumerate(annotations):
        frag = (ann.get("fragment") or "").strip()
        body = ann.get("annotation")
        plain = normalize_whitespace(annotation_to_plain(body))
        title = (frag[:60] + "…") if len(frag) > 60 else frag
        url = ann.get("url") or ""
        refs_pl[key] = {"title": title, "text": plain, "url": url}
        refs_ru[key] = {"title": title, "text": plain, "url": url}

    return {
        "lines_pl": lines_pl,
        "lines_ru": lines_ru,
        "by_line": by_line,
        "refs_pl": refs_pl,
        "refs_ru": refs_ru,
    }


def lyrics_to_html(data):
    """Генерирует HTML блока текста: lyrics-part + lyrics-line-pair."""
    lines_pl = data["lines_pl"]
    lines_ru = data["lines_ru"]
    by_line = data["by_line"]

    out = []
    in_part = False
    for i in range(len(lines_pl)):
        line_pl = lines_pl[i]
        line_ru = lines_ru[i] if i < len(lines_ru) else ""
        is_section = section_label(line_pl)
        if is_section and in_part:
            out.append("</div>")
            in_part = False
        if is_section or not in_part:
            out.append('<div class="lyrics-part">')
            in_part = True
        regs = by_line.get(i, [])
        pl_inner = build_line_html(line_pl, regs)
        # Для русского текста не навешиваем авто-спаны по позициям польского текста,
        # чтобы не ломать разметку перевода. Кликабельные слова сейчас только в польской колонке.
        ru_inner = build_line_html(line_ru, []) if line_ru else ""
        if is_section:
            pl_inner = "<em>%s</em>" % pl_inner
            if line_ru.strip().startswith("["):
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


def refs_to_js(refs_pl, refs_ru):
    """Формирует JS: var referencesPl = {...}; var referencesRu = {...};"""
    def obj_to_js(obj):
        entries = []
        for k, v in sorted(obj.items(), key=lambda x: int(x[0])):
            title_esc = json.dumps(v.get("title", ""), ensure_ascii=False)
            text_esc = json.dumps(v.get("text", ""), ensure_ascii=False)
            url_esc = json.dumps(v.get("url", ""), ensure_ascii=False)
            entries.append("%s: { title: %s, text: %s, url: %s }" % (k, title_esc, text_esc, url_esc))
        return "{\n  " + ",\n  ".join(entries) + "\n}"
    return "var referencesPl = %s;\nvar referencesRu = %s;" % (obj_to_js(refs_pl), obj_to_js(refs_ru))


def main():
    with DATA_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    tracks = data.get("tracks", [])
    base = Path(__file__).parent
    for track in tracks:
        title = track.get("title", "")
        slug = TRACK_SLUGS.get(title)
        if not slug:
            print("Пропуск трека без slug:", title)
            continue
        built = build_track_data(track)
        lyrics_html = lyrics_to_html(built)
        refs_js = refs_to_js(built["refs_pl"], built["refs_ru"])

        html_path = base / (slug + ".html")
        if not html_path.exists():
            print("Файл не найден:", html_path)
            continue

        html_content = html_path.read_text(encoding="utf-8")

        # Подставляем блок текста: ищем <div class="lyrics-text" id="lyricsPolish"> ... </div>
        # или для простых страниц — заменяем lyrics-placeholder и добавляем структуру
        if 'id="lyricsPolish"' in html_content:
            start_marker = 'id="lyricsPolish">'
            start_pos = html_content.find(start_marker)
            if start_pos != -1:
                content_start = start_pos + len(start_marker) + 1  # после ">\n"
                # Ищем закрывающий тег lyrics-text: </div> с отступом 10 пробелов
                end_marker = "\n          </div>"
                end_marker_start = html_content.find(end_marker, content_start)
                if end_marker_start != -1:
                    html_content = (
                        html_content[:content_start]
                        + lyrics_html
                        + html_content[end_marker_start:]
                    )
        else:
            # Страница без lyrics-text: заменяем блок с placeholder на структуру как у szlugi
            placeholder = '<p class="lyrics-placeholder">Текст в разработке.</p>'
            if placeholder in html_content:
                new_block = """<div class="lyrics-main">
        <div class="view-toggles" role="tablist" aria-label="Режим отображения текста">
          <button type="button" class="view-toggle active" data-view="both" aria-pressed="true">Оба языка</button>
          <button type="button" class="view-toggle" data-view="pol" aria-pressed="false">Только польский</button>
          <button type="button" class="view-toggle" data-view="ru" aria-pressed="false">Только русский</button>
        </div>
        <div class="lyrics-columns lyrics-paired" id="lyricsColumns">
          <div class="lyrics-paired-headers">
            <h3 class="lyrics-line-pl">Tekst po polsku</h3>
            <h3 class="lyrics-line-ru">Текст на русском</h3>
          </div>
          <div class="lyrics-text" id="lyricsPolish">
            """
                new_block += lyrics_html
                new_block += """
          </div>
        </div>
      </div>
      <aside class="reference-panel" id="referencePanel">
        <div class="reference-header">
          <h4 id="referenceTitle">Справка</h4>
          <button class="close-reference" id="closeReference" aria-label="Закрыть">×</button>
        </div>
        <div class="reference-content" id="referenceContent">
          <p class="reference-placeholder">Кликни на выделенное слово в тексте, чтобы увидеть справку.</p>
        </div>
      </aside>"""
                # Ищем и заменяем блок от content-wrapper до конца (до </div></div> перед footer)
                cw_start = html_content.find("<div class=\"content-wrapper\">")
                if cw_start == -1:
                    cw_start = html_content.find("<div class='content-wrapper'>")
                if cw_start != -1:
                    # До какого места резать: после content-wrapper идёт lyrics-columns или lyrics-column, ищем закрывающие теги
                    after_cw = html_content.find(">", cw_start) + 1
                    # Ищем конец секции: </div> </div> перед <footer или </section
                    end_search = html_content.find("</footer>", after_cw)
                    if end_search == -1:
                        end_search = html_content.find("</section>", after_cw)
                    if end_search != -1:
                        # Ищем последние два </div> перед end_search
                        last_div = html_content.rfind("</div>", after_cw, end_search)
                        prev_div = html_content.rfind("</div>", after_cw, last_div)
                        # Контент content-wrapper заканчивается перед prev_div (включая prev_div)
                        end_pos = prev_div + len("</div>")
                        html_content = (
                            html_content[: cw_start]
                            + '<div class="content-wrapper" id="contentWrapper">\n      '
                            + new_block
                            + "\n    "
                            + html_content[end_pos:]
                        )
                else:
                    html_content = html_content.replace(
                        '<div class="lyrics-column">\n          <h3>Tekst po polsku</h3>\n          '
                        + placeholder
                        + "\n        </div>\n        <div class=\"lyrics-column\">\n          <h3>Текст на русском</h3>\n          "
                        + placeholder
                        + "\n        </div>",
                        new_block,
                        1,
                    )

        # Вставить или обновить скрипт сносков и track.js
        new_scripts = "  <script>\n" + refs_js + "\n  </script>\n  <script src=\"track.js\"></script>"
        if "track.js" in html_content:
            inline_refs_pattern = re.compile(
                r"  <script>\s*var referencesPl.*?</script>\s*<script src=\"track.js\"></script>",
                re.DOTALL,
            )
            if inline_refs_pattern.search(html_content):
                html_content = inline_refs_pattern.sub(new_scripts, html_content, count=1)
            else:
                html_content = html_content.replace(
                    '  <script src="track.js"></script>',
                    new_scripts,
                    1,
                )
        else:
            html_content = html_content.replace(
                "</body>",
                new_scripts + "\n</body>",
                1,
            )

        html_path.write_text(html_content, encoding="utf-8")
        print("OK:", slug)

    print("Готово.")


if __name__ == "__main__":
    main()
