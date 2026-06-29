# 黑川玲 SDXL LoRA — rei-sdxl-lora

黒川玲（Kurokawa Rei）原创猫娘 OC 的 SDXL LoRA 模型。

## 角色简介

温柔系黑猫猫娘，154cm 娇小身材，黑色超长直发 + 紫色发尾渐变，紫色瞳孔。
黑色项圈 + 猫爪吊坠，紫色蝴蝶结/X 字发夹，学院风宽松外套 + 水手服 + 百褶裙。
详见 [角色设计书](黑川玲_角色设计.txt)。

## 模型信息

| 项目 | 内容 |
|------|------|
| 基底模型 | SDXL 1.0 base |
| LoRA 维度 | rank 32, alpha 16 |
| 训练范围 | UNet only |
| 精度 | bf16 |
| 优化器 | AdamW 8-bit (weight_decay=0.01) |
| 学习率 | 5e-5, cosine scheduler, 50 warmup |
| 训练数据 | 56 张 gpt-image-2 生成图 |
| Epoch | 10 |
| 触发词 | `kurokawa_rei` |

## 使用方式

### ComfyUI

1. 将 `checkpoints/kurokawa_rei_sdxl.safetensors` 放入 `ComfyUI/models/loras/`
2. 加载 SDXL 模型 + 此 LoRA
3. 提示词示例：

```
kurokawa_rei, cat_ears, 1girl, solo, black_hair, very_long_hair, purple_eyes, school_uniform, ...
```

4. LoRA 权重建议从 0.6 开始尝试

### 自动 WebUI

放入 `stable-diffusion-webui/models/Lora/` 目录即可。

## 数据集

- **5 模块渐进结构**: Identity → Pose → Expression → Outfit → Scene
- 图片通过 flux-art.ai 平台的 gpt-image-2 模型生成
- 标签使用 WD14 tagger 自动打标 + `kurokawa_rei` trigger word

## 训练

```bash
python sd-scripts/sdxl_train_network.py \
  --pretrained_model_name_or_path sd_xl_base_1.0.safetensors \
  --train_data_dir ./dataset \
  --network_module networks.lora \
  --network_dim 32 --network_alpha 16 \
  --learning_rate 5e-5 --unet_lr 5e-5 \
  --optimizer_type AdamW8bit \
  --optimizer_args weight_decay=0.01 \
  --lr_scheduler cosine --lr_warmup_steps 50 \
  --mixed_precision bf16 \
  --network_train_unet_only \
  --max_train_epochs 10
```

## 项目结构

```
rei-sdxl-lora/
├── checkpoints/
│   └── kurokawa_rei_sdxl.safetensors   # LoRA 模型 (325MB)
├── dataset/                             # 训练数据集 (56 images + tags)
├── 黑川玲_角色设计.txt                   # 角色设定书
├── flux_gpt-image-2_提示词.txt          # 图片生成提示词
├── tag_standalone.py                    # WD14 打标脚本
└── organize_dataset.py                  # 数据集整理脚本
```

## License

MIT
