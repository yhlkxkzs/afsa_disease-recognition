# yolo5s_seg

**任务**：病害识别（方案 1+2：YOLO-seg 分类 + mask → 病斑面积比 → 程度 L0–L4）

## 模型信息

- `github_model_id`: **`yolo5s_seg`**
- 架构：segmentation / scheme **1+2**
- 类别数：**213**
- 输入尺寸：**640**
- 权重：`best.pt`
- 标签：`labelmap.json`（213 类全局标签）

## 质量评估

*训练指标未记录或 run 未完成。*

**推荐等级**：对比

**说明**：YOLOv5 对照；训练指标未完整记录。

## App / GitHub 对接

- 推理仓目录：`exports/yolo5s_seg/`
- `predictions.json` 中 `github_model_id` 必须为 **`yolo5s_seg`**（与 App 注册表一致）
- 程度字段由 workflow 调用 `scripts/severity.py` 从 mask 面积比计算
