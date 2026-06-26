# 任务 2：病害识别（Disease Classification）+ 方案 1+2 程度后处理

**输入**：病叶 / 病果图片  
**输出**：病害类别（Task A）+ 病斑面积程度 L0–L4（Task B，同一 YOLO-seg 前向 + 规则映射）  
**范式**：YOLO 实例分割（主） / 检测（对照）

与 [fruit_classification](../fruit_classification/README.md) 同模板，数据侧多 **L2/L3 tier** 与 **meta 侧车**。

## 目录

```text
tasks/disease_classification/
├── configs/
│   ├── default.yaml              # 默认 YOLO11s-seg
│   └── models/                   # 10 个方案1+2 对比模型
├── data/                         # 链接/复制自 disease_recognition/manifests
├── docs/
│   ├── DATA_TIERS.md
│   └── MODEL_SELECTION.md
├── exports/                      # best.pt + data.yaml + classes（训练后）
├── incoming/                     # App 上传（待接 GitHub Actions）
├── runs/
└── scripts/
    ├── build_manifest.py         # 同步 registry → data/
    ├── prepare_yolo_dataset.py   # 调用 datasets 仓导出脚本
    ├── severity.py               # Task B：mask/bbox → r → L0–L4
    └── train_yolo.py             # Ultralytics 训练入口
```

## 数据源

| 路径 | 说明 |
|------|------|
| **`APP/AFSA/data/disease_classification/`** | **训练池**（YOLO + meta，与 multistate 同级） |
| `Database/.../disease_recognition/database/` | 源数据（182 集） |
| `Database/.../disease_recognition/manifests/` | 注册表（L2/L3 tier） |
| `tasks/disease_classification/data/` | 链到上面 `data/disease_classification` |

## 快速开始

```bash
cd /home/yuhanlin/APP/AFSA

# 1. 构建注册表与 YOLO 池（在 datasets 仓）
python3 /home/yuhanlin/Database/datasets/disease_recognition/scripts/build_training_registry.py
python3 tasks/disease_classification/scripts/prepare_yolo_dataset.py --tier scheme_12

# 2. 同步 manifest 到本任务 data/
python3 tasks/disease_classification/scripts/build_manifest.py

# 3. 训练（默认 yolo11s-seg）
python3 tasks/disease_classification/scripts/train_yolo.py \
  --model-config tasks/disease_classification/configs/models/yolo11s_seg.yaml
```

## Task A + Task B 衔接

见 [docs/DATA_TIERS.md](docs/DATA_TIERS.md)。推理时调用 `scripts/severity.py` 从预测 mask 计算程度，**无需单独程度标注**。

## exports

见 [exports/MANIFEST.md](exports/MANIFEST.md)。

## GitHub 推理仓

本任务 `exports/` 同步至 [`afsa_disease-recognition`](https://github.com/yhlkxkzs/afsa_disease-recognition)。

```bash
cd tasks/disease_classification
git push origin main
```

大文件（>100 MB）使用 Git LFS：`yolo8m_seg/best.pt`、`yolo9c_seg/best.pt`。
