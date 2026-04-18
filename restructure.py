import os
import shutil

base = "dataset"
splits = ["train", "val", "test"]

for split in splits:
    src_img = os.path.join(base, split, "images")
    src_lbl = os.path.join(base, split, "labels")

    dst_img = os.path.join(base, "images", split)
    dst_lbl = os.path.join(base, "labels", split)

    if not os.path.exists(src_img):
        print(f"❌ {src_img} not found")
        continue

    os.makedirs(dst_img, exist_ok=True)
    os.makedirs(dst_lbl, exist_ok=True)

    print(f"Moving {split} images...")
    for f in os.listdir(src_img):
        shutil.move(os.path.join(src_img, f), os.path.join(dst_img, f))

    print(f"Moving {split} labels...")
    for f in os.listdir(src_lbl):
        shutil.move(os.path.join(src_lbl, f), os.path.join(dst_lbl, f))

print("✅ DONE")