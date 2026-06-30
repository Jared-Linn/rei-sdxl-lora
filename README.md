<p align="center">
  <img src="assets/showcase_portrait.png" alt="黑川玲 Kurokawa Rei" width="512"/>
</p>

<h1 align="center">黑川玲 SDXL LoRA — Kurokawa Rei</h1>

<p align="center">
  <a href="https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0">
    <img src="https://img.shields.io/badge/Base-SDXL_1.0-blue?logo=huggingface" alt="SDXL 1.0"/>
  </a>
  <img src="https://img.shields.io/badge/LoRA-Rank_32_Alpha_16-purple" alt="LoRA Rank 32"/>
  <img src="https://img.shields.io/badge/Dataset-56_Images-green" alt="56 Images"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License"/>
  <img src="https://img.shields.io/badge/Status-v2_Recommended-brightgreen" alt="v2"/>
</p>

<p align="center">
  <b>黑川玲（Kurokawa Rei）</b> — 温柔系黑猫猫娘 OC 的 SDXL LoRA 模型。<br>
  黑色超长直发 · 紫色发尾渐变 · 紫色瞳孔 · 黑猫耳 · 学院风
</p>

---

## ✨ Quick Start

```text
1. 下载 LoRA → checkpoints/kurokawa_rei_sdxl_v2.safetensors
2. 放入 ComfyUI/models/loras/ 或 webui/models/Lora/
3. 加载 SDXL 1.0 base 模型
4. LoRA 权重 = 0.7，CLIP Skip = -2
5. 输入触发词: kurokawa_rei
6. 生成 (Step 30, CFG 7, 1024×1024)
```

---

## 🖼️ Gallery

<table>
  <tr>
    <td align="center"><b>Portrait</b></td>
    <td align="center"><b>Full Body</b></td>
    <td align="center"><b>Refined</b></td>
    <td align="center"><b>High Quality</b></td>
  </tr>
  <tr>
    <td><img src="assets/showcase_portrait.png" width="240"/></td>
    <td><img src="assets/showcase_fullbody.png" width="240"/></td>
    <td><img src="assets/showcase_refined1.png" width="240"/></td>
    <td><img src="assets/showcase_high.png" width="240"/></td>
  </tr>
</table>

---

## 📋 Model Information

### Version Comparison

| | v1 | v2 ✅ |
|---|---|---|
| **File** | `kurokawa_rei_sdxl.safetensors` | `kurokawa_rei_sdxl_v2.safetensors` |
| **Tags** | WD14 auto (~10 generic/image) | Hand-crafted (38-42 character tags/image) |
| **Training** | 10 epochs | 10 epochs |
| **Status** | Legacy | **Recommended** |

### v2 Improvements

- **Full tag rewrite**: ~15 generic WD14 tags → 38-42 precise tags per image
- **All character details captured**: purple gradient hair, pink inner ear, choker, paw pendant, etc.
- **Modular tagging**: Identity / Pose / Expression / Outfit / Scene — each module adds context tags
- **Results**: significantly better character consistency, real cat ears (not headband), clearer clothing details

### Trigger Words

**Required:**
```
kurokawa_rei
```

**Optional (character features):**
```
black_hair, very_long_hair, purple_gradient_hair
purple_eyes, blush, fair_skin
cat_ears, black_cat_ears, pink_inner_ear, ear_fluff
black_choker, paw_pendant
purple_bow, x_hairclip
```

**Optional (outfit):**
```
black_jacket, oversized_jacket, frilled_jacket
black_sailor_uniform, sailor_collar, large_purple_bow
black_pleated_skirt, thighhighs, black_loafers
school_uniform
```

---

## 🎯 Recommended Parameters

| Parameter | Value |
|-----------|-------|
| **Sampler** | DPM++ 2M Karras |
| **Steps** | 28–35 |
| **CFG Scale** | 6–7 |
| **Resolution** | 1024×1024 (SDXL native) |
| **LoRA Weight** | 0.65–0.8 |
| **CLIP Skip** | 2 (SDXL: stop_at_clip_layer = -2) |

> **Tips**:
> - Weight > 0.9 → stronger character features but risk of overfitting
> - Weight < 0.5 → character identity may fade
> - Start at 0.7 and adjust based on your prompt

---

## 💬 Prompt Guide

### Prompt Structure

Build your prompts layer by layer:

```
kurokawa_rei                            ← Trigger
1girl, solo                             ← Character type
standing, cat_paw, head_tilt            ← Pose / Action
smile, looking_at_viewer                ← Expression
school_uniform, black_jacket            ← Outfit
classroom, cherry_blossoms              ← Scene / Background
morning_light, soft_lighting            ← Lighting
masterpiece, best_quality, highres      ← Quality
```

### Example Prompts

#### Portrait

```
kurokawa_rei, 1girl, solo, upper_body, looking_at_viewer, smile,
black_hair, very_long_hair, purple_gradient_hair, purple_eyes,
cat_ears, black_cat_ears, pink_inner_ear, black_choker, paw_pendant,
purple_bow, x_hairclip, blush, fair_skin,
school_uniform, large_purple_bow,
simple_background, soft_lighting,
masterpiece, best_quality
```

#### Full Body

```
kurokawa_rei, 1girl, solo, full_body, standing,
black_hair, very_long_hair, purple_gradient_hair, purple_eyes,
cat_ears, black_cat_ears, tail, black_tail, purple_bow_on_tail,
black_choker, paw_pendant, purple_bow, x_hairclip,
black_jacket, oversized_jacket, frilled_jacket, heart_zipper, paw_badge,
black_sailor_uniform, sailor_collar, large_purple_bow,
black_pleated_skirt, thighhighs, black_loafers,
outdoors, day, city_background,
masterpiece, best_quality, highres
```

#### Classroom

```
kurokawa_rei, 1girl, solo, sitting, looking_at_viewer,
black_hair, very_long_hair, purple_gradient_hair, purple_eyes,
cat_ears, black_cat_ears, tail,
school_uniform, black_jacket,
classroom, desk, window, natural_lighting,
masterpiece, best_quality
```

#### Night Street

```
kurokawa_rei, 1girl, solo, standing, full_body,
black_hair, very_long_hair, purple_eyes,
cat_ears, black_cat_ears, tail,
black_jacket, oversized_jacket, black_pleated_skirt,
night, street_lamp, city, evening,
masterpiece, best_quality
```

#### Cherry Blossom

```
kurokawa_rei, 1girl, solo, walking, looking_at_viewer,
black_hair, very_long_hair, purple_gradient_hair, purple_eyes,
cat_ears, black_cat_ears, tail, black_tail,
school_uniform, black_jacket, thighhighs,
cherry_blossoms, petals, spring, outdoors, day, park,
soft_lighting, masterpiece, best_quality
```

### Negative Prompt

```
nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers,
extra digit, fewer digits, cropped, worst quality, low quality, normal quality,
jpeg artifacts, signature, watermark, username, blurry
```

---

## 🧠 Capabilities

### What the LoRA Learns

| Category | Details |
|----------|---------|
| ✅ **Character Identity** | Face, expression, proportions |
| ✅ **Hair** | Black, very long, straight, purple gradient tips |
| ✅ **Cat Ears** | Black, pink inner, white fluff — **real ears, not headband** |
| ✅ **Cat Tail** | Black tail with purple bow at tip |
| ✅ **Outfit (Default)** | School uniform: jacket + sailor + pleated skirt |
| ✅ **Accessories** | Choker, paw pendant, purple bow, X-hairclip, heart zipper |
| ✅ **Facial Expressions** | Smile, shy, happy, surprised, smug |

### Generalization

| Scenario | Quality |
|----------|---------|
| ✅ Portrait / Upper body | Strong |
| ✅ Full body | Good |
| ✅ Indoor / Classroom | Good |
| ✅ Outdoor / Street | Moderate |
| ✅ Night scene | Moderate |
| ⬜ Different outfits | Partial (more data needed) |

---

## ⚠️ Known Issues

| Condition | Observed Effect |
|-----------|----------------|
| Weight > 0.9 | Hair color saturation too high, slight overfitting on outfit details, cat ear ratio may enlarge |
| Weight < 0.5 | Character identity fades, some details lost |
| CFG > 9 | Overexposed, artifacts |
| Complex backgrounds | Character may blend with background |
| Non-default outfits | Works but less consistent — more outfit data planned |

---

## 📊 Training

- **56 training images** generated via gpt-image-2
- **5 progressive modules**: Identity(10) → Pose(10) → Expression(6) → Outfit(8) → Scene(22)
- **Tags**: 38-42 hand-crafted tags per image in a fixed core + module-specific structure
- **Framework**: kohya_ss / sd-scripts (`sdxl_train_network.py`)
- **Params**: rank 32, alpha 16, UNet only, bf16, AdamW 8-bit, cosine LR, 10 epochs

For full training details, see [TRAINING.md](TRAINING.md).

### Training Pipeline

```
GPT-image-2  ──→  Manual Selection  ──→  Hand-written Tags  ──→  Dataset (56 img)
                                                                        ↓
SDXL 1.0 Base  ──→  kohya_ss / sd-scripts  ←──  Dataset (56 img + .txt)
                          ↓
                    LoRA weights (.safetensors)
                          ↓
                   Evaluation (ComfyUI)
                          ↓
                       v2 Release
```

---

## 📁 Project Structure

```
rei-sdxl-lora/
├── assets/                                   # Screenshots for README
│   ├── showcase_portrait.png
│   ├── showcase_fullbody.png
│   ├── showcase_refined1.png
│   └── showcase_high.png
├── checkpoints/
│   ├── kurokawa_rei_sdxl.safetensors         # v1 LoRA (325MB)
│   └── kurokawa_rei_sdxl_v2.safetensors       # v2 LoRA ✅ (325MB)
├── dataset/                                  # 56 training images + .txt tags
├── kohya_ss_output/
│   └── train_v2.log                          # v2 training log
├── test_output/                              # Local inference tests (gitignored)
├── 黑川玲_角色设计.txt                        # Character design document (Chinese)
├── flux_gpt-image-2_提示词.txt               # GPT-image-2 generation prompts
├── tag_standalone.py                         # WD14 offline tagger (reference)
├── organize_dataset.py                       # Dataset organization script
├── TRAINING.md                               # Training pipeline documentation
└── README.md
```

---

## 🛣️ Roadmap

- ✅ **v1** — Baseline training with WD14 auto-tags
- ✅ **v2** — Full tag rewrite, significantly improved consistency
- ⬜ **v3** *(planned)* — 100+ dataset, more outfits, more dynamic poses
- ⬜ **HuggingFace** — Model card + demo space
- ⬜ **Civitai** — Release with showcase images

---

## 🙏 Credits

| Role | Source |
|------|--------|
| **Base Model** | [SDXL 1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) by Stability AI |
| **Training Framework** | [kohya_ss/sd-scripts](https://github.com/kohya-ss/sd-scripts) |
| **Dataset Generation** | gpt-image-2 (via flux-art.ai) |
| **Character Design** | Original OC by Jared-Linn |

---

## 📜 License

MIT License. You are free to:

- ✅ **Personal use** — Generate images for yourself
- ✅ **Commercial use** — Use in your own projects/products
- ✅ **Fine-tune** — Use as a base for further training
- ✅ **Merge** — Combine with other models/LoRAs
- ✅ **Share** — Redistribute with attribution

You may NOT:

- ❌ Claim authorship of this LoRA
- ❌ Redistribute without attribution

---

<p align="center">
  <sub>黑川玲 © Jared-Linn · Built with SDXL · <a href="https://github.com/Jared-Linn/rei-sdxl-lora">GitHub</a></sub>
</p>
