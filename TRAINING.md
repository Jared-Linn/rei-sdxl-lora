# 黑川玲 SDXL LoRA — 训练流程

> 本文档完整记录了从 0 到 1 训练 SDXL LoRA 的全流程，包含环境搭建、数据集准备、标签策略、训练参数和服务器的所有细节。

---

## 目录

1. [环境搭建](#1-环境搭建)
2. [数据集准备](#2-数据集准备)
3. [标签策略（关键）](#3-标签策略关键)
4. [标签自动生成脚本](#4-标签自动生成脚本)
5. [训练配置详解](#5-训练配置详解)
6. [训练执行](#6-训练执行)
7. [监控与日志](#7-监控与日志)
8. [推理测试](#8-推理测试)
9. [常见问题](#9-常见问题)

---

## 1. 环境搭建

### 1.1 训练框架

使用 [kohya_ss/sd-scripts](https://github.com/kohya-ss/sd-scripts) 中的 `sdxl_train_network.py`。

```bash
git clone https://github.com/kohya-ss/sd-scripts.git
cd sd-scripts
pip install -r requirements.txt

# bitsandbytes 可选（8-bit 优化器需要）
pip install bitsandbytes==0.45.4 --no-deps
```

### 1.2 SDXL 模型下载

国内推荐使用 ModelScope 镜像（速度快）：

```bash
pip install modelscope
python -c "
from modelscope import snapshot_download
snapshot_download('AI-ModelScope/stable-diffusion-xl-base-1.0',
                  cache_dir='/root/autodl-tmp/msc_cache')
# 模型在 sd_xl_base_1.0.safetensors
"
```

或 HuggingFace 镜像：

```bash
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download stabilityai/stable-diffusion-xl-base-1.0 \
  --local-dir /root/autodl-tmp/models/sdxl
```

**硬件要求**: 建议 >= 12GB VRAM（RTX 3080 Ti / 3090 / A5000+）  
**Pascal 架构（TITAN Xp / P100）不支持原生 bf16，训练效率极低，不推荐。**

### 1.3 推荐云 GPU 配置

| 平台 | 推荐机型 | 显存 | 费用参考 |
|------|---------|------|---------|
| AutoDL | RTX 3090 / 3080 Ti | 24G / 12G | ~2-4 元/小时 |
| Seacloud | RTX 3090 | 24G | ~3-5 元/小时 |

训练 56 张图 × 10 epoch 约需 10-15 分钟。

---

## 2. 数据集准备

### 2.1 图像生成

使用 gpt-image-2 模型（flux-art.ai 平台）分模块生成：

```
数据集结构（按生成顺序）：
Module 1: Identity   — 固定服装，多角度（正面/侧身/背面/特写/俯仰拍） → 10 张
Module 2: Pose       — 同服装，不同动作（坐姿/蹲姿/伸手/猫猫拳）    → 10 张
Module 3: Expression — 同服装，不同神态（微笑/害羞/惊讶/坏笑）     → 6 张
Module 4: Outfit     — 新服装，角色特征不变（连衣裙/便服/睡衣）     → 8 张
Module 5: Scene      — 完整环境剧情（校园/户外/夜景/室内）           → 22 张
```

**原则**: 每模块 10-15 张，逐模块推进。Module 1 没出稳前别进 Module 2。

### 2.2 数据整理

`organize_dataset.py` 脚本负责：
- 去重（排除水印图、下载残留等）
- 按模块分组
- 统一命名规则：`kurokawa_rei_{序号}_{模块}.png`

### 2.3 数据集要求

- 图片格式：PNG（推荐）或 JPG
- 分辨率：建议 >= 1024px（SDXL 原生分辨率）
- 图片数量：30-100 张为宜，本 repo 共 56 张
- 标签文件：同名 .txt 文件，每行一个逗号分隔的标签串

---

## 3. 标签策略（关键）

### 3.1 教训：WD14 自动打标不够

第一次训练（v1）使用 WD14 tagger 自动打标，结果是灾难性的：

| 问题 | WD14 标签 | 正确标签 |
|------|-----------|---------|
| 发色 | `pink_hair` ❌ | `black_hair, purple_gradient_hair` |
| 猫耳类型 | `animal_ears` ❌ | `black_cat_ears, pink_inner_ear, ear_fluff` |
| 项圈 | **缺失** | `black_choker, paw_pendant` |
| 服装细节 | **缺失** | `frilled_jacket, sailor_collar, large_purple_bow` |
| 发饰 | **缺失** | `purple_bow, x_hairclip` |

**结论**: WD14 对原创 OC（非 Danbooru 已有角色）效果极差，必须人工撰写标签。

### 3.2 标签结构（v2 方案）

每张图标签分两层：

```
[核心特征] + [模块补充]
```

**核心特征（32 个固定标签）** — 所有图片共享：

```
kurokawa_rei, 1girl, solo,
animal_ears, black_cat_ears, pink_inner_ear, ear_fluff,       # 猫耳
tail, black_tail, purple_bow_on_tail,                          # 尾巴
black_hair, very_long_hair, straight_hair, purple_gradient_hair, # 发型
purple_eyes, blush, fair_skin,                                 # 脸部
black_choker, paw_pendant, purple_bow, x_hairclip,             # 饰品
heart_zipper, paw_badge,                                       # 外套细节
black_jacket, oversized_jacket, frilled_jacket,                # 外套
black_sailor_uniform, sailor_collar, large_purple_bow,         # 内搭
black_pleated_skirt, thighhighs, black_loafers, school_uniform # 下装+鞋子
```

**模块补充** — 按图片模块追加：

| 模块 | 补充标签 |
|------|---------|
| Identity | `looking_at_viewer, smile, simple_background, white_background, upper_body` |
| Pose | `cat_pose, cat_paw, head_tilt, sitting, standing` |
| Expression | `smile, shy, happy, looking_at_viewer, upper_body` |
| Outfit | `looking_at_viewer, smile, simple_background, white_background, upper_body, long_sleeves` |
| Scene | `outdoors, standing, full_body, day, long_sleeves, skirt` |

### 3.3 标签编写原则

1. **先写固定的特征，再写场景/动作** — 保证角色一致性优先
2. **使用的关键词必须是 LoRA 能学会的** — 如 `black_hair` 比 `dark_hair` 好
3. **宁多勿少** — 多标签不会伤害模型，少标签会丢失特征
4. **所有图共享核心特征** — 让模型知道哪些特征总是同时出现
5. **动作/场景标签给模型留组合空间** — 推理时可通过改标签换动作

---

## 4. 标签自动生成脚本

如果数据集较大会手写累，可用以下脚本批量生成：

```python
CORE = [
    "kurokawa_rei", "1girl", "solo",
    "animal_ears", "black_cat_ears", "pink_inner_ear", "ear_fluff",
    "tail", "black_tail", "purple_bow_on_tail",
    "black_hair", "very_long_hair", "straight_hair", "purple_gradient_hair",
    "purple_eyes", "blush", "fair_skin",
    "black_choker", "paw_pendant", "purple_bow", "x_hairclip",
    "heart_zipper", "paw_badge",
    "black_jacket", "oversized_jacket", "frilled_jacket",
    "black_sailor_uniform", "sailor_collar", "large_purple_bow",
    "black_pleated_skirt", "thighhighs", "black_loafers", "school_uniform",
]

MODULE = {
    "Identity":    ["looking_at_viewer","smile","simple_background","white_background","upper_body"],
    "Pose":        ["cat_pose","cat_paw","head_tilt","sitting","standing"],
    "Expression":  ["smile","shy","happy","looking_at_viewer","upper_body"],
    "Outfit":      ["looking_at_viewer","smile","simple_background","white_background","upper_body","long_sleeves"],
    "Scene":       ["outdoors","standing","full_body","day","long_sleeves","skirt"],
}

# 文件名格式: kurokawa_rei_001_Identity.txt
for fname in os.listdir(DATASET):
    if not fname.endswith(".txt"): continue
    module = fname.replace(".txt","").split("_")[-1]  # 从文件名提取模块名
    tags = CORE + MODULE.get(module, [])
    open(os.path.join(DATASET, fname), "w").write(", ".join(tags))
```

---

## 5. 训练配置详解

### 5.1 完整训练命令

```bash
python sdxl_train_network.py \
  --pretrained_model_name_or_path /path/to/sd_xl_base_1.0.safetensors \
  --train_data_dir /path/to/dataset \
  --output_dir /path/to/output \
  --output_name kurokawa_rei_sdxl_v2 \
  --network_module networks.lora \
  --network_dim 32 \
  --network_alpha 16 \
  --resolution 1024 \
  --train_batch_size 1 \
  --max_train_epochs 10 \
  --learning_rate 5e-5 \
  --unet_lr 5e-5 \
  --optimizer_type AdamW8bit \
  --optimizer_args weight_decay=0.01 \
  --lr_scheduler cosine \
  --lr_warmup_steps 50 \
  --mixed_precision bf16 \
  --max_grad_norm 1.0 \
  --save_every_n_epochs 1 \
  --save_last_n_epochs 5 \
  --enable_bucket \
  --min_bucket_reso 512 \
  --max_bucket_reso 1024 \
  --bucket_no_upscale \
  --cache_latents \
  --skip_cache_check \
  --gradient_checkpointing \
  --shuffle_caption \
  --caption_extension .txt \
  --network_train_unet_only \
  --log_with tensorboard
```

### 5.2 参数详解

#### 核心参数

| 参数 | 本配置 | 说明 |
|------|--------|------|
| `network_dim` | 32 | LoRA 秩（rank）。越大模型容量越大但文件也大。32 是 SDXL LoRA 常用值 |
| `network_alpha` | 16 | LoRA alpha。权重缩放用，`alpha/rank` 是有效缩放系数 |
| `network_train_unet_only` | 启用 | 只训练 UNet，不训练 Text Encoder。可节省显存 |
| `resolution` | 1024 | SDXL 原生分辨率 |
| `train_batch_size` | 1 | 批大小 1 是 12GB 显存的极限 |

#### 优化器

| 参数 | 值 | 说明 |
|------|----|------|
| `optimizer_type` | AdamW8bit | 8-bit AdamW 省一半优化器显存 |
| `weight_decay` | 0.01 | 正则化防过拟合，LoRA 训练推荐 |
| `learning_rate` | 5e-5 | SDXL LoRA 常用 LR |
| `lr_scheduler` | cosine | 余弦退火，收敛更平滑 |
| `lr_warmup_steps` | 50 | 预热防止初期梯度爆炸 |

#### 精度

| 参数 | 值 | 说明 |
|------|----|------|
| `mixed_precision` | bf16 | BF16 混合精度。**要求 Ampere 架构以上显卡（RTX 30xx+）** |

**重要**: Pascal 架构（GTX 10xx, TITAN Xp, P100）不支持原生 BF16。虽然 PyTorch 有软件模拟但会导致 OOM、系统无响应等严重问题。Pascal 用户要用 fp16。

#### Bucket 训练

```bash
--enable_bucket           # 启用多分辨率 bucketing
--min_bucket_reso 512     # 最小 bucket 分辨率
--max_bucket_reso 1024    # 最大 bucket 分辨率（SDXL 原生）
--bucket_no_upscale       # 不放大图片（只缩小）
```

Bucket 允许训练不同长宽比的图片（正方形、竖图、横图），将相似尺寸分组到同一 batch，提高训练效率。

#### 其他

| 参数 | 说明 |
|------|------|
| `cache_latents` | 预计算 VAE latent 到硬盘，节省训练时显存 |
| `gradient_checkpointing` | 激活检查点，省显存换时间 |
| `shuffle_caption` | 训练时随机打乱标签顺序，增强泛化 |
| `caption_extension .txt` | 指定标签文件后缀 |

---

## 6. 训练执行

### 6.1 启动训练

```bash
cd sd-scripts
python sdxl_train_network.py ...  # 上面的完整命令
```

### 6.2 训练过程

- bf16 + batch_size=1 + 12GB VRAM 下约 1 分钟/epoch（56 张图）
- 10 epoch 总计约 10-12 分钟
- 每 epoch 保存一次 checkpoint
- 保留最后 5 个 epoch 的 checkpoint

### 6.3 验证训练成果

训练结束后检查 LoRA 权重：

```python
from safetensors.torch import load_file

sd = load_file("output/kurokawa_rei_sdxl_v2.safetensors")

# 统计
n_params = len(sd)
nonzero = sum((v != 0).sum().item() for v in sd.values())
total = sum(v.numel() for v in sd.values())
mean_abs = sum(v.abs().mean().item() for v in sd.values()) / n_params
has_nan = any(v.isnan().any().item() for v in sd.values())
has_inf = any(v.isinf().any().item() for v in sd.values())

print(f"Parameters:   {n_params}")
print(f"Non-zero:     {nonzero}/{total} ({100*nonzero/total:.1f}%)")
print(f"Mean abs:     {mean_abs:.6f}")
print(f"NaN/Inf:      {has_nan}/{has_inf}")
```

正常输出示例：
```
Parameters:   120
Non-zero:     45957120/45957120 (100.0%)
Mean abs:     0.000777
NaN/Inf:      False/False
```

---

## 7. 监控与日志

### 7.1 TensorBoard

训练命令加 `--log_with tensorboard` 后，可用 TensorBoard 查看 loss 曲线：

```bash
tensorboard --logdir logs --port 6006
```

### 7.2 Loss 曲线解读

- 正常：loss 从 ~0.1 平滑下降至 ~0.02-0.03
- 过拟合：loss 先降后升（或 validation loss 不再下降）
- 欠拟合：loss 停留在高位（>0.1）

### 7.3 训练日志

`kohya_ss_output/train_v2.log` 包含完整训练输出，可作为参考。

---

## 8. 推理测试

### 8.1 ComfyUI 测试

推荐使用 ComfyUI 进行快速推理测试。关键流程：

```
CheckpointLoader → SDXL base 1.0
       ↓
LoraLoader → 加载 LoRA，权重 0.6-0.8
       ↓
CLIPSetLastLayer → stop_at_clip_layer = -2
       ↓
[正向提示词] → CLIPTextEncode
[负向提示词] → CLIPTextEncode
       ↓
EmptyLatentImage → 1024×1024
       ↓
KSampler → steps=30, cfg=7, sampler=euler
       ↓
VAEDecode → SaveImage
```

### 8.2 Diffusers（离线 Python 推理）

参见 [README.md](README.md#diffusers-python) 中的代码示例。

### 8.3 LoRA 权重调整

- **0.5-0.6**: 保守，保留更多基底模型风格
- **0.7-0.8**: 推荐，角色一致性较好
- **0.9-1.0**: 激进，角色特征强但可能过拟合

### 8.4 推荐测试提示词

简单正面：
```
kurokawa_rei, 1girl, solo, black_hair, very_long_hair, purple_eyes,
cat_ears, black_cat_ears, black_choker, school_uniform,
looking_at_viewer, smile, simple_background
```

全身测试：
```
kurokawa_rei, 1girl, solo, black_hair, purple_eyes, cat_ears,
black_jacket, oversized_jacket, frilled_jacket,
black_sailor_uniform, large_purple_bow, black_pleated_skirt,
thighhighs, black_loafers, standing, full_body,
outdoors, day, city_background
```

---

## 9. 常见问题

### 9.1 训练崩了 / SSH 无响应

**现象**: SSH 连不上，面板显示 CPU 占满但 GPU 不动  
**原因**: OOM + SWAP 撑爆  
**解决方案**:
- 检查显存：`nvidia-smi`（至少保留 2GB 空闲）
- 检查是否用了 bf16（Pascal 架构不支持 → 换 fp16）
- 降低 batch_size 到 1
- 开启 `--gradient_checkpointing`
- 开启 `--cache_latents`

### 9.2 猫耳生成像头饰

**原因**: 训练标签缺少 `animal_ears`, `black_cat_ears`, `pink_inner_ear` 等猫耳细节标签  
**解决**: 确保每张图的标签都包含猫耳描述

### 9.3 衣服颜色混淆

**原因**: 标签没区分外套和内搭  
**解决**: 确保标签同时包含 `black_jacket`（外套）和 `black_sailor_uniform`（内搭水手服）

### 9.4 LoRA 权重太低

检查 `mean_abs` 值：
- `mean_abs < 0.0001`: 权重太低，可能没学到
- `mean_abs ~ 0.0005-0.001`: 正常范围
- `mean_abs > 0.01`: 可能过拟合

### 9.5 权重下载和导入

从服务器下载 LoRA：
```bash
scp -P 30705 root@server:/root/autodl-tmp/output/kurokawa_rei_sdxl_v2.safetensors ./
```

### 9.6 服务器配置备忘

| 项目 | 值 |
|------|-----|
| SSH 端口 | 不固定，看云平台分配的端口 |
| 数据路径 | `/root/autodl-tmp/` |
| 模型路径 | `/root/autodl-tmp/models/sdxl/` |
| 数据集路径 | `/root/autodl-tmp/dataset/` |
| 输出路径 | `/root/autodl-tmp/output/` |
| kohya_ss 路径 | `/root/autodl-tmp/kohya_ss/sd-scripts/` |
| ComfyUI 路径 | `/root/ComfyUI/` |

---

## 附录

### A. 文件命名规范

```
kurokawa_rei_{序号}_{模块}.png
kurokawa_rei_{序号}_{模块}.txt
```

序号 3 位（001-056），模块名首字母大写：Identity / Pose / Expression / Outfit / Scene

### B. 参考链接

- [kohya_ss/sd-scripts](https://github.com/kohya-ss/sd-scripts) — 训练框架
- [SDXL 1.0 base](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) — 基底模型
- [ModelScope 镜像](https://modelscope.cn/models/AI-ModelScope/stable-diffusion-xl-base-1.0) — 国内快速下载
- [自动打标模型 WD14](https://huggingface.co/SmilingWolf/wd-v1-4-swinv2-tagger-v2) — 参考用
