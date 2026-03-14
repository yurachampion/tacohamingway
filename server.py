# -*- coding: utf-8 -*-
"""
Локальный сервер для админки: API content.json + загрузка картинок.
Запуск: py server.py  →  http://127.0.0.1:5000/admin
"""
import json
import re
import os
from pathlib import Path
from flask import Flask, send_from_directory, request, jsonify

BASE = Path(__file__).resolve().parent
CONTENT_PATH = BASE / "data" / "content.json"
UPLOAD_DIR = BASE / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = Flask(__name__, static_folder=str(BASE), static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB


def get_content():
    if not CONTENT_PATH.exists():
        return {"tracks": {}}
    return json.loads(CONTENT_PATH.read_text(encoding="utf-8"))


def save_content(data):
    CONTENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONTENT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


@app.route("/api/content", methods=["GET"])
def api_get_content():
    return jsonify(get_content())


@app.route("/api/content", methods=["POST"])
def api_save_content():
    data = request.get_json()
    if not data or "tracks" not in data:
        return jsonify({"ok": False, "error": "Invalid body"}), 400
    save_content(data)
    return jsonify({"ok": True})


def allowed_file(filename):
    ext = (Path(filename).suffix or "").lower()
    return ext in {".jpg", ".jpeg", ".png", ".gif", ".webp"}


@app.route("/api/upload", methods=["POST"])
def api_upload():
    if "file" not in request.files:
        return jsonify({"ok": False, "error": "No file"}), 400
    f = request.files["file"]
    if not f.filename or not allowed_file(f.filename):
        return jsonify({"ok": False, "error": "Invalid or missing file"}), 400
    safe_name = re.sub(r"[^\w\-.]", "_", f.filename)
    path = UPLOAD_DIR / safe_name
    f.save(str(path))
    # Возвращаем URL-путь для подстановки в content (от корня сайта)
    url_path = "/uploads/" + safe_name
    return jsonify({"ok": True, "path": url_path})


@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/admin")
def admin():
    return send_from_directory(BASE, "admin.html")


@app.route("/")
def index():
    return send_from_directory(BASE, "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(BASE, path)


if __name__ == "__main__":
    print("Admin: http://127.0.0.1:5000/admin")
    app.run(host="127.0.0.1", port=5000, debug=True)
