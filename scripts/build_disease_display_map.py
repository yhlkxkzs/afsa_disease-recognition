#!/usr/bin/env python3
"""Build disease_display_map.json (213 classes, en + zh) for GitHub inference & App."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABELMAP = ROOT / "exports" / "yolo8m_seg" / "labelmap.json"
OVERRIDES_ZH = ROOT / "data" / "disease_zh_overrides.json"
OVERRIDES_EN = ROOT / "data" / "disease_en_overrides.json"
OUT = ROOT / ".github" / "scripts" / "disease_display_map.json"

DISEASE_ZH_PARTS: dict[str, str] = {
    "anthracnose": "炭疽病",
    "scab": "黑星病",
    "brown_rot": "褐腐病",
    "brown_spot": "褐斑病",
    "powdery_mildew": "白粉病",
    "downy_mildew": "霜霉病",
    "gray_mold": "灰霉病",
    "leaf_spot": "叶斑病",
    "rust": "锈病",
    "late_blight": "晚疫病",
    "early_blight": "早疫病",
    "root_rot": "根腐病",
    "black_rot": "黑腐病",
    "canker": "溃疡病",
    "greening": "黄龙病",
    "blackspot": "黑星病",
    "blight": "疫病",
    "mosaic": "花叶病",
    "virus": "病毒病",
    "spot": "斑点病",
    "rot": "腐烂病",
    "disease": "病害",
    "pest": "虫害",
    "borer": "蛀虫",
    "thrip": "蓟马",
    "beetle": "甲虫",
    "aphid": "蚜虫",
    "healthy": "健康",
    "health": "健康",
}

FRUIT_ZH_PARTS: dict[str, str] = {
    "apple": "苹果",
    "pear": "梨",
    "peach": "桃",
    "grape": "葡萄",
    "orange": "橙",
    "citrus": "柑橘",
    "mango": "芒果",
    "strawberry": "草莓",
    "tomato": "番茄",
    "potato": "马铃薯",
    "corn": "玉米",
    "watermelon": "西瓜",
    "guava": "番石榴",
    "papaya": "木瓜",
    "pomegranate": "石榴",
    "blueberry": "蓝莓",
    "cherry": "樱桃",
    "banana": "香蕉",
    "eggplant": "茄子",
    "pepper": "辣椒",
    "cucumber": "黄瓜",
    "soybean": "大豆",
    "cassava": "木薯",
    "kiwi": "猕猴桃",
}


def title_en(key: str) -> str:
    return key.replace("_", " ").strip().title()


def is_healthy(key: str) -> bool:
    k = key.lower()
    return k in {"healthy", "health"} or "healthy" in k


def infer_zh(key: str) -> str:
    parts = [p for p in key.lower().split("_") if p]
    if is_healthy(key):
        for p in parts:
            if p in FRUIT_ZH_PARTS:
                return f"{FRUIT_ZH_PARTS[p]}健康"
        return "健康"
    zh_bits: list[str] = []
    for p in parts:
        if p in FRUIT_ZH_PARTS:
            zh_bits.append(FRUIT_ZH_PARTS[p])
        elif p in DISEASE_ZH_PARTS:
            zh_bits.append(DISEASE_ZH_PARTS[p])
    if zh_bits:
        return "".join(zh_bits)
    return title_en(key)


def infer_en(key: str) -> str:
    if is_healthy(key):
        parts = key.lower().split("_")
        for p in parts:
            if p in FRUIT_ZH_PARTS:
                return f"Healthy {title_en(p)}"
        return "Healthy"
    return title_en(key)


def load_overrides(path: Path) -> dict[str, str]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def main() -> None:
    names = json.loads(LABELMAP.read_text(encoding="utf-8")).get("names") or []
    zh_over = load_overrides(OVERRIDES_ZH)
    en_over = load_overrides(OVERRIDES_EN)
    classes: dict[str, dict[str, str]] = {}
    for raw in names:
        key = str(raw).strip()
        if not key or key == "_":
            continue
        classes[key] = {
            "en": en_over.get(key, infer_en(key)),
            "zh": zh_over.get(key, infer_zh(key)),
        }
    payload = {
        "version": 1,
        "description": "Map YOLO disease class slug to display names (en + zh); 213 scheme-1+2 classes",
        "classes": classes,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(classes)} classes)")


if __name__ == "__main__":
    main()
