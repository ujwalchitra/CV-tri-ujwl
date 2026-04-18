import os
import xml.etree.ElementTree as ET
import shutil
import random

# ✅ Correct paths based on your setup
base_path = "dataset/train"
img_dir = os.path.join(base_path, "images")
xml_dir = os.path.join(base_path, "annotations/xmls")  # FIXED here

# Output folder (YOLO format)
output_base = "processed_dataset"

train_ratio = 0.8

# Convert XML bbox to YOLO format
def convert(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    return x * dw, y * dh, w * dw, h * dh

# Load XML files
files = os.listdir(xml_dir)
random.shuffle(files)

# Split train/val
split_index = int(len(files) * train_ratio)
train_files = files[:split_index]
val_files = files[split_index:]

def process(files, split):
    out_img = os.path.join(output_base, "images", split)
    out_lbl = os.path.join(output_base, "labels", split)

    os.makedirs(out_img, exist_ok=True)
    os.makedirs(out_lbl, exist_ok=True)

    for file in files:
        tree = ET.parse(os.path.join(xml_dir, file))
        root = tree.getroot()

        filename = root.find("filename").text

        size = root.find("size")
        w = int(size.find("width").text)
        h = int(size.find("height").text)

        label_path = os.path.join(out_lbl, file.replace(".xml", ".txt"))

        has_pothole = False

        with open(label_path, "w") as f:
            for obj in root.iter("object"):
                cls = obj.find("name").text

                # Only keep pothole class (D40)
                if cls != "D40":
                    continue

                has_pothole = True

                xmlbox = obj.find("bndbox")
                xmin = float(xmlbox.find("xmin").text)
                xmax = float(xmlbox.find("xmax").text)
                ymin = float(xmlbox.find("ymin").text)
                ymax = float(xmlbox.find("ymax").text)

                bb = convert((w, h), (xmin, xmax, ymin, ymax))
                f.write(f"0 {' '.join(map(str, bb))}\n")

        # Copy image only if pothole exists
        if has_pothole:
            src_img = os.path.join(img_dir, filename)
            dst_img = os.path.join(out_img, filename)

            if os.path.exists(src_img):
                shutil.copy(src_img, dst_img)
        else:
            os.remove(label_path)

print("Processing train...")
process(train_files, "train")

print("Processing val...")
process(val_files, "val")

print("✅ DONE")