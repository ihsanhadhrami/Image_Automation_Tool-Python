# 📸 Image Automation & Enhancement Engine (Python)

A **batch image processing engine** built with Python that applies **iPhone/Lightroom-style adjustments** (exposure, contrast, saturation, highlights, shadows, sharpness) **consistently at scale**.

This tool focuses on **automation, consistency, and production readiness**, rather than manual one-by-one editing.

---

## Key Features

- Batch image processing
- iPhone-style image adjustments
- Gamma-based highlights & shadows (no harsh clipping)
- Fault-tolerant pipeline (one failure won’t stop the batch)
- Config-driven adjustments
- Optimized output for web usage

---

## Architecture Overview
Input Images
↓
Resize
↓
Adjustments (Exposure → Contrast → Saturation → Highlights → Shadows → Sharpness)
↓
Watermark
↓
Optimized Output


---

## Folder Structure
Img_editor/
├─ image_automation_tool.py
├─ watermark.png
├─ process.log
├─ input_imgs/
└─ output_imgs/


---

## Configuration Example

```python
ADJUSTMENTS = {
    "exposure": -0.1,
    "contrast": 0.2,
    "saturation": 0.15,
    "sharpness": 0.2,
    "highlights": -0.25,
    "shadows": 0.25
}
Values are normalized to prevent over-processing and visual artifacts.


Design Highlights

Uses relative paths for portability
Non-destructive, sequential adjustment pipeline
Curve-based tone mapping for natural results
Defensive error handling with logging

Use Cases
E-commerce product images
Marketing & social media assets
Photographer batch editing
Web image optimization
Dataset preparation

Tech Stack
Python · Pillow (PIL) · NumPy


---

Note

This is an automation engine, not a mobile photo editor — built for scale, consistency, and reliability.



