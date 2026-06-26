# yolo8m_seg

**任务**：病害识别（方案 1+2：YOLO-seg 分类 + mask → 病斑面积比 → 程度 L0–L4）

## 模型信息

- `github_model_id`: **`yolo8m_seg`**
- 架构：segmentation / scheme **1+2**
- 类别数：**213**
- 输入尺寸：**640**
- 权重：`best.pt`
- 标签：`labelmap.json`（213 类全局标签）

## 质量评估

| 指标 | Bbox | Mask |
|------|------|------|
| 最佳 epoch | 83 | 83 |
| Precision | 0.7087 | 0.7123 |
| Recall | 0.6905 | 0.6756 |
| mAP50 | 0.7178 | 0.7086 |
| mAP50-95 | 0.5467 | 0.5129 |

**推荐等级**：⭐ 首选

**说明**：213 类方案 1+2 当前最佳；mask mAP50≈0.71，精度与召回均衡，建议作为 App 主模型槽位。

## App / GitHub 对接

- 推理仓目录：`exports/yolo8m_seg/`
- `predictions.json` 中 `github_model_id` 必须为 **`yolo8m_seg`**（与 App 注册表一致）
- 程度字段由 workflow 调用 `scripts/severity.py` 从 mask 面积比计算
