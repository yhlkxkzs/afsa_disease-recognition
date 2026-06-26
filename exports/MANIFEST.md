# exports — disease_classification (YOLO scheme 1+2)

训练完成后每个模型目录：

```text
exports/<model_id>/
├── best.pt
├── data.yaml
├── labelmap.json      # 213 类全局标签
├── export_info.json   # 指标与元数据
└── README.md
```

## 已上传模型（2026-06-25）

| `github_model_id` | 架构 | mask mAP50 | mask mAP50-95 | 推荐 |
|-------------------|------|------------|---------------|------|
| `yolo8m_seg` | YOLOv8m-seg | **0.709** | **0.513** | ⭐ 首选 |
| `yolo9c_seg` | YOLOv9c-seg | 0.637 | 0.451 | 次选 |
| `yolo11m_seg` | YOLOv11m-seg | 0.569 | 0.397 | 稳定重训版 |
| `yolo8n_seg` | YOLOv8n-seg | 0.411 | 0.271 | 轻量 |
| `yolo11n_seg` | YOLOv11n-seg | 0.376 | 0.247 | 轻量 |
| `yolo10s_seg` | YOLOv10s-seg | 0.325 | 0.203 | 对比 |
| `yolo5s_seg` | YOLOv5s-seg | — | — | 对比 |
| `yolo8s_seg` | YOLOv8s-seg | 0.183* | 0.109* | 早停，仅供参考 |
| `yolo11s_seg` | YOLOv11s-seg | 0.162* | 0.096* | 早停，仅供参考 |
| `yolo11s_detect` | YOLOv11s-detect | — | — | 仅检测无 mask |

\* 指标来自早停/不稳定 run，不作为上线首选。

主模型槽位（待定）：`production_yolo8m_seg/`（当前最佳 `yolo8m_seg`）

Task B 程度逻辑在 `scripts/severity.py`，不单独导出程度模型。
