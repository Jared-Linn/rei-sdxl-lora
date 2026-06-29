# 黑川玲 SDXL LoRA — rei-sdxl-lora

[黑川玲（Kurokawa Rei）](黑川玲_角色设计.txt) 原创猫娘 OC 的 SDXL LoRA 模型。

**模型版本**: v2（改进标签重训版）  
**基底模型**: [SDXL 1.0 base](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)

## 角色简介

温柔系黑猫猫娘，154cm 娇小身材，黑色超长直发 + 紫色发尾渐变，紫色瞳孔。  
黑色项圈 + 猫爪吊坠，紫色蝴蝶结 / X 字发夹，学院风宽松外套 + 水手服 + 百褶裙。

核心辨识元素：
- 黑猫耳（粉色内耳、白色绒毛）— **真猫耳，不是头饰**
- 黑色猫尾 + 尾尖紫色蝴蝶结
- 黑色项圈 + 紫色猫爪吊坠
- 紫色蝴蝶结发饰 + X 字发夹
- 黑色学院风宽松外套 + 紫色爱心拉链吊饰
- 黑色水手服 + 胸前紫色大蝴蝶结

详见 [完整角色设计书](黑川玲_角色设计.txt)。

## 模型版本对比

| 项目 | v1 | v2 ✅ |
|------|-----|-------|
| LoRA 文件 | `kurokawa_rei_sdxl.safetensors` | `kurokawa_rei_sdxl_v2.safetensors` |
| 标签质量 | WD14 自动打标（~10 通用标签/张） | 人工撰写（38-42 角色专属标签/张） |
| 训练时间 | ~10 epoch | ~10 epoch |
| 状态 | 旧版 | **当前推荐版本** |

### v2 改进点

- **标签重写**: 每张图从 ~15 个通用标签 → 38-42 个精准标签，包含所有角色特征（紫色渐变发、猫耳内耳粉色、项圈猫爪吊坠、爱心拉链等）
- **模块化标签**: Identity / Pose / Expression / Outfit / Scene 五模块，每模块追加场景相关标签
- **效果**: 角色一致性显著提升，猫耳不再是头饰效果，服装细节更清晰

## 使用方式

### ComfyUI

1. 将 `checkpoints/` 下的 `.safetensors` 文件放入 `ComfyUI/models/loras/`
2. 加载 SDXL 模型 + LoRA loader
3. 推荐提示词结构：

```
kurokawa_rei, 1girl, solo, black_hair, very_long_hair, purple_gradient_hair,
purple_eyes, cat_ears, black_cat_ears, pink_inner_ear, black_choker,
black_jacket, oversized_jacket, school_uniform, ...
```

**LoRA 权重建议**: 0.6 ~ 0.8  
**CLIP skip**: -2（使用 SDXL 建议设置）

### Stable Diffusion WebUI (A1111)

放入 `stable-diffusion-webui/models/Lora/` 目录。

### Diffusers (Python)

```python
from diffusers import StableDiffusionXLPipeline
from safetensors.torch import load_file
import torch

pipe = StableDiffusionXLPipeline.from_single_file(
    "sd_xl_base_1.0.safetensors",
    torch_dtype=torch.bfloat16, use_safetensors=True
).to("cuda")

# 手动融合 LoRA
sd = load_file("checkpoints/kurokawa_rei_sdxl_v2.safetensors")
lora_scale = 0.7 * (16.0 / 32.0)  # strength * (alpha / rank)
sd = {k: v.to("cuda", torch.bfloat16) * lora_scale for k, v in sd.items()}

for name, param in pipe.unet.named_parameters():
    lora_key = name.replace(".", "_")
    down_key = lora_key + ".lora_down.weight"
    up_key = lora_key + ".lora_up.weight"
    if down_key in sd and up_key in sd:
        down, up = sd[down_key], sd[up_key]
        if down.shape[0] == param.shape[0]:
            param.data += (up @ down).reshape(param.shape)

# 生成
prompt = "kurokawa_rei, 1girl, solo, black_hair, cat_ears, ..."
image = pipe(prompt, num_inference_steps=30, guidance_scale=7).images[0]
image.save("output.png")
```

### 负面提示词

通用负面：
```
nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers,
extra digit, fewer digits, cropped, worst quality, low quality, normal quality,
jpeg artifacts, signature, watermark, username, blurry
```

## 数据集

- **56 张训练图像**，由 gpt-image-2 模型生成
- **5 模块渐进结构**：Identity(10) → Pose(10) → Expression(6) → Outfit(8) → Scene(22)
- **标签**: 每张图 38-42 个标签，先写角色核心特征，再追加模块专属标签
- 详见 [训练流程文档](TRAINING.md)

## 模型参数

| 参数 | 值 |
|------|-----|
| 框架 | kohya_ss / sd-scripts |
| LoRA 维度 | rank 32, alpha 16 |
| 训练范围 | UNet only |
| 精度 | bf16 |
| 优化器 | AdamW 8-bit (weight_decay=0.01) |
| 学习率 | 5e-5, cosine scheduler, 50 steps warmup |
| 分辨率 | 1024 × 1024 (bucket 512-1024) |
| 触发词 | `kurokawa_rei` |

## 项目结构

```
rei-sdxl-lora/
├── checkpoints/
│   ├── kurokawa_rei_sdxl.safetensors      # v1 LoRA (325MB)
│   └── kurokawa_rei_sdxl_v2.safetensors    # v2 LoRA ✅ (325MB)
├── dataset/                # 56 训练图像 + .txt 标签文件
├── kohya_ss_output/
│   └── train_v2.log        # v2 训练日志
├── 黑川玲_角色设计.txt       # 完整角色设定书
├── flux_gpt-image-2_提示词.txt  # gpt-image-2 生成提示词
├── tag_standalone.py       # WD14 离线打标脚本（参考用）
├── organize_dataset.py     # 数据集整理脚本
├── TRAINING.md             # 完整训练流程文档
└── README.md
```

## 测试图片

`test_output/` 包含两轮训练的测试生成结果（v1 和 v2）。

## License

MIT
