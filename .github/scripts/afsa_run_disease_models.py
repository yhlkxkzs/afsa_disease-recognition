#!/usr/bin/env python3
"""Run all disease YOLO models listed in models_manifest.json on changed images."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
MANIFEST = SCRIPT_DIR / "models_manifest.json"

from afsa_write_predictions import OUT, append_row, ensure_parent

try:
    from ultralytics import YOLO
except ImportError as exc:
    raise SystemExit("pip install ultralytics") from exc

THRESHOLDS = [
    (0.01, 0),
    (0.05, 1),
    (0.15, 2),
    (0.30, 3),
    (1.01, 4),
]

SEVERITY_LABELS_ZH = {
    0: "无/健康",
    1: "极轻",
    2: "轻度",
    3: "中度",
    4: "重度",
}

SEVERITY_LABELS_EN = {
    0: "None/Healthy",
    1: "Very Mild",
    2: "Mild",
    3: "Moderate",
    4: "Severe",
}


def ratio_to_level(ratio: float, *, healthy: bool = False) -> int:
    if healthy or ratio < 0.01:
        return 0
    for bound, level in THRESHOLDS:
        if ratio < bound:
            return level
    return 4


def is_healthy_class(raw_class: str) -> bool:
    key = raw_class.lower()
    return key in {"healthy", "health"} or "healthy" in key


def display_fields(raw_class: str) -> dict:
    en = raw_class.replace("_", " ").strip().title()
    zh = "健康" if is_healthy_class(raw_class) else en
    return {
        "raw_class": raw_class,
        "predicted_class": zh,
        "predicted_class_zh": zh,
        "predicted_class_en": en,
    }


def load_class_names(export_dir: Path) -> list[str]:
    labelmap = export_dir / "labelmap.json"
    if labelmap.is_file():
        meta = json.loads(labelmap.read_text(encoding="utf-8"))
        names = meta.get("names") or []
        if names:
            return [str(x) for x in names]
    info = export_dir / "export_info.json"
    if info.is_file():
        meta = json.loads(info.read_text(encoding="utf-8"))
        nc = int(meta.get("nc") or 0)
        if nc:
            return [str(i) for i in range(nc)]
    return []


def model_is_segmentation(export_dir: Path) -> bool:
    info = export_dir / "export_info.json"
    if info.is_file():
        meta = json.loads(info.read_text(encoding="utf-8"))
        return meta.get("task_type") != "detection"
    return "-seg" in export_dir.name or export_dir.name.endswith("_seg")


def severity_fields(result, det_idx: int, *, healthy: bool, is_seg: bool) -> dict:
    if healthy:
        return {
            "area_ratio": 0.0,
            "severity_level": 0,
            "predicted_state": SEVERITY_LABELS_ZH[0],
            "predicted_state_zh": SEVERITY_LABELS_ZH[0],
            "predicted_state_en": SEVERITY_LABELS_EN[0],
        }

    h, w = result.orig_shape
    box = result.boxes.xyxy[det_idx].cpu().numpy()
    x1, y1, x2, y2 = box
    bbox_area = max(float((x2 - x1) * (y2 - y1)), 1.0)

    if is_seg and result.masks is not None:
        mask = result.masks.data[det_idx].cpu().numpy()
        mask = cv2.resize(mask, (w, h), interpolation=cv2.INTER_LINEAR)
        mask_area = float((mask > 0.5).sum())
        ratio = min(mask_area / bbox_area, 1.0)
    else:
        ratio = min(bbox_area / float(max(h * w, 1)), 1.0)

    level = ratio_to_level(ratio, healthy=healthy)
    return {
        "area_ratio": round(ratio, 6),
        "severity_level": level,
        "predicted_state": SEVERITY_LABELS_ZH[level],
        "predicted_state_zh": SEVERITY_LABELS_ZH[level],
        "predicted_state_en": SEVERITY_LABELS_EN[level],
    }


def predict_one(model: YOLO, img_path: Path, class_names: list[str], *, is_seg: bool, conf: float = 0.25) -> dict | None:
    results = model.predict(source=str(img_path), conf=conf, verbose=False)
    result = results[0]
    if result.boxes is None or len(result.boxes) == 0:
        return None

    confs = result.boxes.conf.cpu().numpy()
    det_idx = int(np.argmax(confs))
    cls_id = int(result.boxes.cls[det_idx].cpu().numpy())
    confidence = float(confs[det_idx])
    raw_class = class_names[cls_id] if 0 <= cls_id < len(class_names) else str(cls_id)

    row = display_fields(raw_class)
    row["confidence"] = confidence
    healthy = is_healthy_class(raw_class)
    if is_seg:
        row.update(severity_fields(result, det_idx, healthy=healthy, is_seg=True))
    return row


def load_routes(images_file: Path) -> list[dict]:
    routes_file = Path("/tmp/afsa_routes.json")
    if routes_file.is_file():
        data = json.loads(routes_file.read_text(encoding="utf-8"))
        routes = data.get("routes") or []
        if routes:
            return routes
    routes = []
    for line in images_file.read_text(encoding="utf-8").splitlines():
        p = line.strip()
        if p:
            routes.append({"image_path": p, "task_type": "disease_classification"})
    return routes


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: afsa_run_disease_models.py /tmp/images.txt", file=sys.stderr)
        sys.exit(2)

    images_file = Path(sys.argv[1])
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    exports_root = REPO_ROOT / manifest.get("exports_root", "exports")
    routes = [r for r in load_routes(images_file) if str(r.get("task_type", "")).startswith("disease")]
    if not routes:
        print("[error] no disease routes to run (check sidecar task_type)", file=sys.stderr)
        sys.exit(1)

    ensure_parent()
    OUT.write_text(json.dumps({"predictions": []}, indent=2) + "\n", encoding="utf-8")

    for spec in manifest.get("disease_models", []):
        github_model_id = spec["github_model_id"]
        export_dir = exports_root / spec["export_dir"]
        pt = export_dir / "best.pt"
        if not pt.is_file():
            print(f"[skip] missing {pt}")
            continue

        is_seg = model_is_segmentation(export_dir)
        class_names = load_class_names(export_dir)
        try:
            model = YOLO(str(pt))
        except Exception as exc:
            print(f"[skip] load failed {github_model_id}: {exc}")
            continue

        for route in routes:
            rel = route["image_path"]
            img_path = REPO_ROOT / rel
            if not img_path.is_file():
                print(f"[warn] missing image {img_path}")
                continue

            pred = predict_one(model, img_path, class_names, is_seg=is_seg)
            if pred is None:
                pred = {
                    "raw_class": "none",
                    "predicted_class": "未检测到病害",
                    "predicted_class_zh": "未检测到病害",
                    "predicted_class_en": "No Detection",
                    "confidence": 0.0,
                }
                if is_seg:
                    pred.update(
                        {
                            "area_ratio": 0.0,
                            "severity_level": 0,
                            "predicted_state": SEVERITY_LABELS_ZH[0],
                            "predicted_state_zh": SEVERITY_LABELS_ZH[0],
                            "predicted_state_en": SEVERITY_LABELS_EN[0],
                        }
                    )

            append_row(
                {
                    "image": route["image_path"],
                    "github_path": route["image_path"],
                    "afsa_detection_id": route.get("afsa_detection_id"),
                    "github_model_id": github_model_id,
                    **pred,
                }
            )

        print(f"[ok] {github_model_id} routes={len(routes)}")


if __name__ == "__main__":
    main()
