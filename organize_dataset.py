"""
黑川玲 LoRA 训练集 —— 整理脚本
功能：筛图 + 统一重命名 + 按模块分组写入文件夹
打标在服务器用 kohya_ss 做
"""
import shutil
from pathlib import Path

SRC = Path(r"I:\vm\share\hermes agent\ComfyUI生图\lora 训练\黑川玲")
DST = Path(r"I:\vm\share\hermes agent\ComfyUI生图\lora 训练\黑川玲_training")

TRIGGER = "kurokawa_rei"

EXCLUDE_NAMES = {
    "立绘.png", "多视角.png", "标准工业三视图.png",
}

modules = ["Identity", "Pose", "Expression", "Outfit", "Scene"]

# 清空重建
if DST.exists():
    shutil.rmtree(DST)
DST.mkdir(parents=True)

idx = 0
for mod in modules:
    mod_dir = SRC / mod
    if not mod_dir.exists():
        continue
    for f in sorted(mod_dir.iterdir()):
        if f.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            continue
        if f.name in EXCLUDE_NAMES:
            print(f"  [X] exlude: {mod}/{f.name}")
            continue
        if f.name.endswith("_download.png") or f.name.startswith("wm_"):
            print(f"  [X] exlude: {mod}/{f.name}")
            continue
        # 复制并重命名
        idx += 1
        ext = f.suffix.lower()
        new_name = f"{TRIGGER}_{idx:03d}_{mod}{ext}"
        shutil.copy2(f, DST / new_name)
        print(f"  [OK] {idx:02d} {mod}/{f.name} -> {new_name}")

print(f"\n共 {idx} 张图片 -> {DST}")
print("[提示] 打标在服务器上做。kohya_ss 自带 WD14 tagger。")
