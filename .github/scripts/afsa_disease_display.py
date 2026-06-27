#!/usr/bin/env python3
"""Resolve YOLO disease class slug → bilingual display labels."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
MAP_PATH = SCRIPT_DIR / "disease_display_map.json"


@lru_cache(maxsize=1)
def load_map() -> dict:
    if not MAP_PATH.is_file():
        return {"classes": {}}
    return json.loads(MAP_PATH.read_text(encoding="utf-8"))


def disease_display(raw: str) -> dict[str, str]:
    key = (raw or "").strip()
    data = load_map()
    info = (data.get("classes") or {}).get(key) or {}
    en = info.get("en") or key.replace("_", " ").title()
    zh = info.get("zh") or en
    return {
        "raw_class": key,
        "predicted_class_en": en,
        "predicted_class_zh": zh,
        "predicted_class": zh,
    }
