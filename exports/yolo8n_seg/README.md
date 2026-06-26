# yolo8n_seg

**任务**：病害识别（方案 1+2：YOLO-seg 分类 + mask → 病斑面积比 → 程度 L0–L4）

## 模型信息

- `github_model_id`: **`yolo8n_seg`**
- 架构：segmentation / scheme **1+2**
- 类别数：**213**
- 输入尺寸：**640**
- 权重：`best.pt`
- 标签：`labelmap.json`（213 类全局标签）

## 质量评估

| 指标 | Bbox | Mask |
|------|------|------|
| 最佳 epoch | 100 | 100 |
| Precision | 0.4976 | 0.4945 |
| Recall | 0.4247 | 0.4195 |
| mAP50 | 0.4163 | 0.4110 |
| mAP50-95 | 0.2907 | 0.2714 |

**推荐等级**：轻量

**说明**：参数量小、推理快，精度中等，适合端侧或对比。

## App / GitHub 对接

- 推理仓目录：`exports/yolo8n_seg/`
- `predictions.json` 中 `github_model_id` 必须为 **`yolo8n_seg`**（与 App 注册表一致）
- 程度字段由 workflow 调用 `scripts/severity.py` 从 mask 面积比计算
