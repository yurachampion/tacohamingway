# -*- coding: utf-8 -*-
"""
Извлекает сноски из текущих HTML треков и формирует начальный data/content.json.
Ключи в content — только те, что реально есть в data-key на странице.
"""
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TRACKS = [
    "szlugi-i-kalafiory",
    "marsz-marsz",
    "wszystko-jedno",
    "trojkat",
    "przerywnik",
    "mieso",
    "900729",
]


def extract_quoted(s, start):
    """Из строки s с позиции start (после открывающей \") ищем закрывающую \", возвращаем (value, end_pos)."""
    if start >= len(s) or s[start] != '"':
        return "", start
    pos = start + 1
    chunks = []
    while pos < len(s):
        if s[pos] == '\\' and pos + 1 < len(s):
            n = s[pos + 1]
            if n == 'n':
                chunks.append('\n')
            elif n == 't':
                chunks.append('\t')
            elif n == '"':
                chunks.append('"')
            else:
                chunks.append(n)
            pos += 2
            continue
        if s[pos] == '"':
            return "".join(chunks), pos + 1
        chunks.append(s[pos])
        pos += 1
    return "".join(chunks), pos


def parse_ref_object(s, pos):
    """Парсит один объект { title: "...", text: "...", url: "..." } из s начиная с pos. Возвращает (dict, end_pos)."""
    if pos >= len(s) or s[pos] != '{':
        return {}, pos
    pos = pos + 1
    out = {"title": "", "text": "", "url": ""}
    while pos < len(s):
        while pos < len(s) and s[pos] in ' \t\n,':
            pos += 1
        if pos >= len(s) or s[pos] == '}':
            return out, pos + (1 if pos < len(s) else 0)
        key_m = re.match(r'(title|text|url)\s*:\s*"', s[pos:])
        if not key_m:
            pos += 1
            continue
        key = key_m.group(1)
        pos += len(key_m.group(0)) - 1
        val, pos = extract_quoted(s, pos)
        out[key] = val
    return out, pos


def extract_refs_block(html, var_name):
    """Достаёт из HTML блок var var_name = { ... }; как строку между { и парной }."""
    pattern = "var %s = " % var_name
    idx = html.find(pattern)
    if idx == -1:
        return None
    idx = html.find("{", idx)
    if idx == -1:
        return None
    start = idx
    depth = 1
    idx += 1
    while idx < len(html) and depth:
        if html[idx] == '{':
            depth += 1
        elif html[idx] == '}':
            depth -= 1
        idx += 1
    return html[start:idx] if depth == 0 else None


def parse_refs_block(block):
    """Парсит блок { 0: {...}, 1: {...} } в словарь key -> {title, text, url}."""
    if not block or block[0] != '{':
        return {}
    refs = {}
    pos = 1
    while pos < len(block):
        while pos < len(block) and block[pos] in ' \t\n,':
            pos += 1
        if pos >= len(block) or block[pos] == '}':
            break
        num_m = re.match(r'(\d+)\s*:\s*\{', block[pos:])
        if not num_m:
            pos += 1
            continue
        key = int(num_m.group(1))
        pos += len(num_m.group(0)) - 1
        obj, pos = parse_ref_object(block, pos)
        refs[key] = obj
    return refs


def extract_keys_from_html(html):
    """Все data-key из страницы."""
    return set(int(m) for m in re.findall(r'data-key="(\d+)"', html))


def main():
    content = {"tracks": {}}
    for slug in TRACKS:
        path = BASE / (slug + ".html")
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        keys_used = extract_keys_from_html(html)
        block_pl = extract_refs_block(html, "referencesPl")
        block_ru = extract_refs_block(html, "referencesRu")
        refs_pl = parse_refs_block(block_pl) if block_pl else {}
        refs_ru = parse_refs_block(block_ru) if block_ru else {}
        footnotes = {}
        for k in sorted(keys_used):
            pl = refs_pl.get(k, {})
            ru = refs_ru.get(k, {})
            footnotes[str(k)] = {
                "title_pl": pl.get("title", ""),
                "title_ru": ru.get("title", ""),
                "text_pl": pl.get("text", ""),
                "text_ru": ru.get("text", ""),
                "url": pl.get("url") or ru.get("url") or "",
                "image": None,
                "video": None,
            }
        content["tracks"][slug] = {"footnotes": footnotes}
    out_path = BASE / "data" / "content.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Written:", out_path)
    total = sum(len(t["footnotes"]) for t in content["tracks"].values())
    print("Total footnotes:", total)


if __name__ == "__main__":
    main()
