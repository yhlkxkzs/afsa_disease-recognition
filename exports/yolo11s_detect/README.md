# yolo11s_detect

**任务**：病害识别（方案 1+2：YOLO-seg 分类 + mask → 病斑面积比 → 程度 L0–L4）

## 模型信息

- `github_model_id`: **`yolo11s_detect`**
- 架构：detection / scheme **1+2**
- 类别数：**213**
- 输入尺寸：**640**
- 权重：`best.pt`
- 标签：`labelmap.json`（213 类全局标签）

## 质量评估

| 指标 | Bbox | Mask |
|------|------|------|
| 最佳 epoch | 5 | 5 |
| Precision | 0.5720 | — |
| Recall | 0.4314 | — |
| mAP50 | 0.4353 | — |
| mAP50-95 | 0.3049 | — |

**推荐等级**：仅检测对照

**说明**：detect 头无 mask，无法输出病斑面积程度（方案 1+2 不完整）。

> detect 模型仅输出 bbox，无 mask；程度需 mask/bbox 面积比，本模型**不适合**作为方案 1+2 主模型。

## App / GitHub 对接

- 推理仓目录：`exports/yolo11s_detect/`
- `predictions.json` 中 `github_model_id` 必须为 **`yolo11s_detect`**（与 App 注册表一致）
- 程度字段由 workflow 调用 `scripts/severity.py` 从 mask 面积比计算
