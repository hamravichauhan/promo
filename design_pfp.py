"""
High-Resolution Profile Avatar (PFP) Generator for @extrovertnerd.dev.
Renders an executive, high-contrast 1024x1024 developer & agency branding emblem.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

SIZE = 1024


def get_font(weight: str, size: int):
    weights = {
        "black": "Montserrat-Black.ttf",
        "extrabold": "Montserrat-ExtraBold.ttf",
        "bold": "Montserrat-Bold.ttf",
        "semibold": "Montserrat-SemiBold.ttf",
    }
    p = os.path.join(FONTS_DIR, weights.get(weight, "Montserrat-Bold.ttf"))
    if os.path.exists(p):
        return ImageFont.truetype(p, size=size)
    return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Black.ttf", size=size)


def generate_pfp(out_path: str = None) -> str:
    if not out_path:
        out_path = os.path.join(OUTPUT_DIR, "extrovertnerd_pfp.jpg")

    img = Image.new("RGBA", (SIZE, SIZE), (8, 12, 20, 255))
    d = ImageDraw.Draw(img)

    # 1. Subtle Radial Glow in Center
    cx, cy = SIZE // 2, SIZE // 2
    for r in range(480, 0, -4):
        alpha = int(45 * (1 - (r / 480)))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(6, 182, 212, alpha))

    # 2. Outer Concentric Neon Rings
    # Outer thin ring
    d.ellipse([cx - 420, cy - 420, cx + 420, cy + 420], outline=(30, 41, 59, 255), width=4)
    # Vibrant Cyan / Emerald Ring
    d.ellipse([cx - 390, cy - 390, cx + 390, cy + 390], outline=(16, 185, 129, 255), width=10)
    # Inner accent ring
    d.ellipse([cx - 365, cy - 365, cx + 365, cy + 365], outline=(6, 182, 212, 180), width=4)

    # 3. 4 Corner Micro Tech Accents (HUD tick marks)
    ticks = [0, 90, 180, 270]
    for angle in ticks:
        rad = math.radians(angle)
        x1 = cx + int(390 * math.cos(rad))
        y1 = cy + int(390 * math.sin(rad))
        x2 = cx + int(440 * math.cos(rad))
        y2 = cy + int(440 * math.sin(rad))
        d.line([(x1, y1), (x2, y2)], fill=(245, 158, 11), width=6)

    # 4. Central Tech Monogram: "</>" and "EN"
    # Glowing Code Bracket Symbol
    f_code = get_font("black", 210)
    code_sym = "</>"
    cw = d.textlength(code_sym, font=f_code)

    # Glow shadow
    d.text((cx - (cw / 2) + 2, cy - 180 + 2), code_sym, font=f_code, fill=(6, 182, 212, 100))
    # Foreground text with gradient color
    d.text((cx - (cw / 2), cy - 180), code_sym, font=f_code, fill=(255, 255, 255))

    # Clean divider bar
    d.rounded_rectangle([cx - 240, cy + 50, cx + 240, cy + 58], radius=4, fill=(16, 185, 129))

    # Brand Title: "EXTROVERTNERD"
    f_title = get_font("black", 62)
    title_str = "EXTROVERTNERD"
    tw = d.textlength(title_str, font=f_title)
    d.text((cx - (tw / 2), cy + 85), title_str, font=f_title, fill=(255, 255, 255))

    # Sub-Pill: ".DEV"
    f_dev = get_font("extrabold", 42)
    dev_str = "⚡ WEB ARCHITECTURE ⚡"
    dw = d.textlength(dev_str, font=f_dev)
    d.rounded_rectangle([cx - (dw / 2) - 25, cy + 175, cx + (dw / 2) + 25, cy + 240], radius=12, fill=(16, 24, 38), outline=(6, 182, 212), width=3)
    d.text((cx - (dw / 2), cy + 188), dev_str, font=f_dev, fill=(6, 182, 212))

    # Convert to RGB and save
    final_pfp = img.convert("RGB")
    final_pfp.save(out_path, quality=95)
    print(f"✨ Profile Picture generated: {out_path}")
    return out_path


if __name__ == "__main__":
    generate_pfp()
