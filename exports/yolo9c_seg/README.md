# yolo9c_seg

**任务**：病害识别（方案 1+2：YOLO-seg 分类 + mask → 病斑面积比 → 程度 L0–L4）

## 模型信息

- `github_model_id`: **`yolo9c_seg`**
- 架构：segmentation / scheme **1+2**
- 类别数：**213**
- 输入尺寸：**640**
- 权重：`best.pt`
- 标签：`labelmap.json`（213 类全局标签）

## 质量评估

| 指标 | Bbox | Mask |
|------|------|------|
| 最佳 epoch | 31 | 31 |
| Precision | 0.6935 | 0.6804 |
| Recall | 0.6117 | 0.6058 |
| mAP50 | 0.6485 | 0.6366 |
| mAP50-95 | 0.4836 | 0.4510 |

**推荐等级**：次选

**说明**：表现仅次于 yolo8m_seg，可作为精度/速度折中备选。

## App / GitHub 对接

- 推理仓目录：`exports/yolo9c_seg/`
- `predictions.json` 中 `github_model_id` 必须为 **`yolo9c_seg`**（与 App 注册表一致）
- 程度字段由 workflow 调用 `scripts/severity.py` 从 mask 面积比计算
