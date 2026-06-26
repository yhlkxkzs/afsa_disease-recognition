# yolo11s_seg

**任务**：病害识别（方案 1+2：YOLO-seg 分类 + mask → 病斑面积比 → 程度 L0–L4）

## 模型信息

- `github_model_id`: **`yolo11s_seg`**
- 架构：segmentation / scheme **1+2**
- 类别数：**213**
- 输入尺寸：**640**
- 权重：`best.pt`
- 标签：`labelmap.json`（213 类全局标签）

## 质量评估

| 指标 | Bbox | Mask |
|------|------|------|
| 最佳 epoch | 1 | 1 |
| Precision | 0.5744 | 0.5705 |
| Recall | 0.1904 | 0.1878 |
| mAP50 | 0.1651 | 0.1618 |
| mAP50-95 | 0.1026 | 0.0956 |

**推荐等级**：仅供参考

**说明**：早停/不稳定 run，mask mAP50≈0.16，不建议上线。

## App / GitHub 对接

- 推理仓目录：`exports/yolo11s_seg/`
- `predictions.json` 中 `github_model_id` 必须为 **`yolo11s_seg`**（与 App 注册表一致）
- 程度字段由 workflow 调用 `scripts/severity.py` 从 mask 面积比计算
