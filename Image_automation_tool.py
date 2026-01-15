from PIL import Image, ImageFilter
from PIL import ImageEnhance
import os
import numpy as np
import logging

logging.basicConfig(
    filename="process.log",
    level=logging.WARNING,
    format="%(asctime)s - %(message)s"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_DIR = os.path.join(BASE_DIR, 'input_imgs')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output_imgs')
WATERMARK_PATH = os.path.join(BASE_DIR, 'watermark.png')
MAX_WIDTH = 1200
QUALITY = 85

os.makedirs(OUTPUT_DIR, exist_ok=True)

def adjust_exposure(img, factor):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(1 + factor)

def adjust_contrast(img, factor):
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(1 + factor)

def adjust_saturation(img, factor):
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(1 + factor)

def adjust_sharpness(img, factor):
    enhancer = ImageEnhance.Sharpness(img)
    return enhancer.enhance(1 + factor)

def adjust_highlights(img, factor):
    np_img = np.array(img)
    mask = np_img > 200
    np_img[mask] = np.clip(np_img[mask] * (1 - factor), 0, 255)
    return Image.fromarray(np_img.astype('uint8'))

def adjust_shadows(img, factor):
    np_img = np.array(img)
    mask = np_img < 50
    np_img[mask] = np.clip(np_img[mask] * (1 + factor), 0, 255)
    return Image.fromarray(np_img.astype('uint8'))

def resize_image(img):
    if img.width > MAX_WIDTH:
        ratio = MAX_WIDTH / img.width
        new_size = (MAX_WIDTH, int(img.height * ratio))
        return img.resize(new_size, Image.LANCZOS)
    return img

def add_watermark(img, watermark):
    img = img.convert("RGBA")
    watermark = watermark.resize((200, 200))
    position = (img.width - watermark.width - 20, img.height - watermark.height - 20)
    img.paste(watermark, position, watermark)
    return img.convert("RGB")

ADJUSTMENTS = {
    "exposure": -0.1,
    "contrast": 0.2,
    "saturation": 0.15,
    "sharpness": 0.2,
    "highlights": -0.25,
    "shadows": 0.25
}


def safe_apply(func, img, factor, name):
    if factor == 0:
        return img
    try:
        return func(img, factor)
    except Exception as e:
        logging.warning(f"{name} failed: {e}")
        return img


watermark = Image.open(WATERMARK_PATH).convert("RGBA")

if not os.path.exists(INPUT_DIR):
    print("❌ input_imgs folder not found.")
    print("➡️ Please create 'input_imgs' and add images.")
    input("Press Enter to exit...")
    exit()

if not any(fname.lower().endswith(('.jpg', '.jpeg', '.png')) for fname in os.listdir(INPUT_DIR)):
    print("❌ No images found in input_imgs.")
    print("➡️ Please add images and run again.")
    input("Press Enter to exit...")
    exit()


for filename in os.listdir(INPUT_DIR):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue


    try:
        img_path = os.path.join(INPUT_DIR, filename)
        img = Image.open(img_path)

        # 1️⃣ Resize dulu
        img = resize_image(img)

        # 2️⃣ Adjustment pipeline (iPhone-style)
        img = safe_apply(adjust_exposure, img, ADJUSTMENTS["exposure"], "Exposure")
        img = safe_apply(adjust_contrast, img, ADJUSTMENTS["contrast"], "Contrast")
        img = safe_apply(adjust_saturation, img, ADJUSTMENTS["saturation"], "Saturation")
        img = safe_apply(adjust_highlights, img, ADJUSTMENTS["highlights"], "Highlights")
        img = safe_apply(adjust_shadows, img, ADJUSTMENTS["shadows"], "Shadows")
        img = safe_apply(adjust_sharpness, img, ADJUSTMENTS["sharpness"], "Sharpness")

        # 3️⃣ Watermark LAST
        img = add_watermark(img, watermark)

        name = os.path.splitext(filename)[0]
        output_path = os.path.join(OUTPUT_DIR, f"{name}_optimized.jpg")

        img.save(output_path, optimize=True, quality=QUALITY)
        print(f"✔ Processed: {filename}")

    except Exception as e:
        print(f"✖ Failed: {filename} | {e}")

print("🚀 All images processed successfully")