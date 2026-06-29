"""
Standalone WD14 tagger
"""
import os, csv, json
from pathlib import Path
import torch
from safetensors.torch import load_file
from PIL import Image
from timm import create_model
from huggingface_hub import hf_hub_download
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize
from tqdm import tqdm

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

MODEL_ID = "SmilingWolf/wd-v1-4-swinv2-tagger-v2"
DATASET = Path(r"I:\vm\share\hermes agent\ComfyUI生图\lora 训练\黑川玲_training")
CACHE = str(DATASET.parent / "wd14_cache")
TRIGGER = "kurokawa_rei"
THRESH = 0.35
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")

# Download
print("Downloading model...")
model_path = hf_hub_download(MODEL_ID, "model.safetensors", cache_dir=CACHE)
tags_path = hf_hub_download(MODEL_ID, "selected_tags.csv", cache_dir=CACHE)

# Load tags
with open(tags_path, encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    tags = [row[1] for row in reader]
print(f"Tags: {len(tags)}")

# Model
print("Loading model...")
model = create_model(
    "swinv2_base_window8_256",
    pretrained=False,
    num_classes=len(tags),
    global_pool="avg",
    img_size=448,
    strict_img_size=False,
)
model.load_state_dict(load_file(model_path), strict=False)
model = model.to(device).eval()
print("Model loaded")

# Transform
transform = Compose([
    Resize(448, interpolation=Image.BICUBIC),
    CenterCrop(448),
    ToTensor(),
    Normalize(mean=[0.5]*3, std=[0.5]*3),
])

# Tag
images = sorted(DATASET.glob("*.png")) + sorted(DATASET.glob("*.jpg"))
print(f"Tagging {len(images)} images...")

for img_path in tqdm(images):
    img = Image.open(img_path).convert("RGB")
    x = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(x)
    probs = torch.sigmoid(logits.squeeze()).cpu().numpy()
    tag_names = [tags[i] for i, p in enumerate(probs) if p >= THRESH]
    img_path.with_suffix(".txt").write_text(
        f"{TRIGGER}, {', '.join(tag_names)}", encoding="utf-8"
    )

print(f"\nDone! Sample:")
txt = list(DATASET.glob("*.txt"))[0].read_text(encoding="utf-8")
print(txt[:200])
