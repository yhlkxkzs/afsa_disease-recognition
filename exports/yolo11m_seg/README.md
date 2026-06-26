# yolo11m_seg

**任务**：病害识别（方案 1+2：YOLO-seg 分类 + mask → 病斑面积比 → 程度 L0–L4）

## 模型信息

- `github_model_id`: **`yolo11m_seg`**
- 架构：segmentation / scheme **1+2**
- 类别数：**213**
- 输入尺寸：**640**
- 权重：`best.pt`
- 标签：`labelmap.json`（213 类全局标签）

## 质量评估

| 指标 | Bbox | Mask |
|------|------|------|
| 最佳 epoch | 20 | 20 |
| Precision | 0.6300 | 0.6247 |
| Recall | 0.5648 | 0.5592 |
| mAP50 | 0.5760 | 0.5692 |
| mAP50-95 | 0.4244 | 0.3973 |

**推荐等级**：稳定重训版

**说明**：稳定 profile 重训后 mask mAP50≈0.57，213 类任务上属于合理水平。

## App / GitHub 对接

- 推理仓目录：`exports/yolo11m_seg/`
- `predictions.json` 中 `github_model_id` 必须为 **`yolo11m_seg`**（与 App 注册表一致）
- 程度字段由 workflow 调用 `scripts/severity.py` 从 mask 面积比计算
