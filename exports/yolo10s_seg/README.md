# yolo10s_seg

**任务**：病害识别（方案 1+2：YOLO-seg 分类 + mask → 病斑面积比 → 程度 L0–L4）

## 模型信息

- `github_model_id`: **`yolo10s_seg`**
- 架构：segmentation / scheme **1+2**
- 类别数：**213**
- 输入尺寸：**640**
- 权重：`best.pt`
- 标签：`labelmap.json`（213 类全局标签）

## 质量评估

| 指标 | Bbox | Mask |
|------|------|------|
| 最佳 epoch | 20 | 20 |
| Precision | 0.5217 | 0.5177 |
| Recall | 0.3544 | 0.3507 |
| mAP50 | 0.3306 | 0.3254 |
| mAP50-95 | 0.2168 | 0.2027 |

**推荐等级**：对比

**说明**：small 体量对比模型。

## App / GitHub 对接

- 推理仓目录：`exports/yolo10s_seg/`
- `predictions.json` 中 `github_model_id` 必须为 **`yolo10s_seg`**（与 App 注册表一致）
- 程度字段由 workflow 调用 `scripts/severity.py` 从 mask 面积比计算
