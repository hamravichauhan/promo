"""
High-Precision Graphic Design Engine for 100-Day Web Playbook Posters.
Renders senior-agency-grade 4:5 Instagram posters with REAL EDITORIAL PHOTOGRAPHY,
giant bold hook typography, interactive visual components, and executive client acquisition.
Master resolution: 2160x2700 downsampled with Lanczos to 1080x1350 for retina crispness.
"""

import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

W, H = 2160, 2700  # Master 2x resolution

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
PHOTOS_DIR = os.path.join(BASE_DIR, "photos")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(FONTS_DIR, exist_ok=True)
os.makedirs(PHOTOS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Curated High-Resolution Editorial Photography Catalog (1800px+ Unsplash CDN)
PHOTO_CATALOG = {
    "laptop_code": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1800&q=85",
    "developer_desk": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1800&q=85",
    "server_rack": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1800&q=85",
    "mobile_device": "https://images.unsplash.com/photo-1551650975-87deedd944c3?w=1800&q=85",
    "analytics_monitor": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1800&q=85",
    "agency_team": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1800&q=85",
    "cloud_network": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1800&q=85",
    "developer_dark": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1800&q=85",
    "wireframe_design": "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=1800&q=85",
    "modern_office": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=1800&q=85",
    "speed_light": "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1800&q=85",
    "custom_tech": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1800&q=85",
}

# Track to Photo Key mapping
TRACK_PHOTO_MAP = {
    "SPEED & CORE WEB VITALS": ["server_rack", "speed_light", "laptop_code", "cloud_network"],
    "LANDING PAGE CONVERSION": ["developer_desk", "wireframe_design", "agency_team", "modern_office"],
    "MOBILE UI & ERGONOMICS": ["mobile_device", "wireframe_design", "developer_dark"],
    "CUSTOM TOOLS & AUTOMATION": ["custom_tech", "analytics_monitor", "developer_dark", "laptop_code"],
    "COPYWRITING & HIERARCHY": ["developer_desk", "wireframe_design", "modern_office"],
    "FORMS & LEAD GENERATION": ["laptop_code", "mobile_device", "agency_team"],
    "MODERN ARCHITECTURE": ["developer_dark", "server_rack", "cloud_network"],
    "WEBSITE AUDIT & ROI": ["analytics_monitor", "agency_team", "modern_office"],
}


def get_font(weight: str, size: int) -> ImageFont.ImageFont:
    """Loads bundled Montserrat fonts across all environments."""
    weights_map = {
        "black": "Montserrat-Black.ttf",
        "extrabold": "Montserrat-ExtraBold.ttf",
        "bold": "Montserrat-Bold.ttf",
        "semibold": "Montserrat-SemiBold.ttf",
        "medium": "Montserrat-Medium.ttf",
        "regular": "Montserrat-Regular.ttf",
    }
    fname = weights_map.get(weight.lower(), "Montserrat-Bold.ttf")
    font_path = os.path.join(FONTS_DIR, fname)
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size=size)
        except Exception:
            pass

    # System fallbacks
    for sys_font in [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]:
        if os.path.exists(sys_font):
            try:
                return ImageFont.truetype(sys_font, size=size)
            except Exception:
                continue

    return ImageFont.load_default()


def wrap_text_to_lines(text: str, font: ImageFont.ImageFont, max_width: int, draw: ImageDraw.ImageDraw) -> list:
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = current_line + [word]
        w = draw.textlength(" ".join(test_line), font=font)
        if w > max_width and current_line:
            lines.append(" ".join(current_line))
            current_line = [word]
        else:
            current_line = test_line
    if current_line:
        lines.append(" ".join(current_line))
    return lines


def ensure_photo(photo_key: str) -> str:
    """Ensures the real high-res photograph is cached locally in photos/."""
    target_path = os.path.join(PHOTOS_DIR, f"{photo_key}.jpg")
    if os.path.exists(target_path) and os.path.getsize(target_path) > 10000:
        return target_path

    url = PHOTO_CATALOG.get(photo_key, PHOTO_CATALOG["laptop_code"])
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
        if r.status_code == 200 and len(r.content) > 10000:
            with open(target_path, "wb") as f:
                f.write(r.content)
            return target_path
    except Exception as e:
        print(f"[-] Photo fetch error for {photo_key}: {e}")

    for f in os.listdir(PHOTOS_DIR):
        if f.endswith(".jpg"):
            return os.path.join(PHOTOS_DIR, f)
    return target_path


def render_poster(day_data: dict, theme_name: str = "dark", out_path: str = None) -> str:
    """
    Renders a photo-backed, magazine-grade 4:5 Instagram poster.
    Combines real high-res photography with bold hook typography and executive agency acquisition.
    """
    day_num = day_data.get("day", 1)
    track = day_data.get("track", "SPEED & CORE WEB VITALS")

    if not out_path:
        out_path = os.path.join(OUTPUT_DIR, f"day_{day_num:03d}_playbook_{theme_name}.jpg")

    # 1. Resolve Real Photo
    photo_key = day_data.get("photo_key")
    if not photo_key:
        pool = TRACK_PHOTO_MAP.get(track, ["laptop_code", "developer_desk", "server_rack"])
        photo_key = pool[(day_num - 1) % len(pool)]

    photo_path = ensure_photo(photo_key)

    # 2. Base HD Photo with Cinematic Cover Crop
    try:
        with Image.open(photo_path) as raw_img:
            raw_img = raw_img.convert("RGBA")
            raw_img = ImageOps.exif_transpose(raw_img)
            bw, bh = raw_img.size
            target_ratio = W / H
            if (bw / bh) > target_ratio:
                crop_w = int(bh * target_ratio)
                cropped = raw_img.crop(((bw - crop_w) // 2, 0, (bw + crop_w) // 2, bh))
            else:
                crop_h = int(bw / target_ratio)
                cropped = raw_img.crop((0, (bh - crop_h) // 2, bw, (bh + crop_h) // 2))
            bg = cropped.resize((W, H), Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"[-] Error loading photo {photo_path}: {e}")
        bg = Image.new("RGBA", (W, H), (10, 14, 22, 255))

    # 3. Cinematic Editorial Gradients
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_ov = ImageDraw.Draw(overlay)

    # Top brand header shade (0 to 440px)
    for y in range(440):
        alpha = int(230 * (1 - (y / 440)))
        d_ov.line([(0, y), (W, y)], fill=(6, 8, 12, alpha))

    # Middle tint (440 to 1100px) - allows real photo details to shine through with dramatic mood
    for y in range(440, 1100):
        d_ov.line([(0, y), (W, y)], fill=(6, 8, 12, 55))

    # Deep bottom gradient (1100px to bottom) - ensures 100% legibility for takeaways & CTA
    for y in range(1100, H):
        progress = (y - 1100) / (H - 1100)
        alpha = int(255 * (progress ** 0.8))
        d_ov.line([(0, y), (W, y)], fill=(7, 9, 14, min(252, alpha)))

    canvas = Image.alpha_composite(bg, overlay).convert("RGB")
    d = ImageDraw.Draw(canvas)

    # 4. Typography Scale
    f_day = get_font("black", 38)
    f_meta = get_font("bold", 34)
    f_handle = get_font("extrabold", 38)
    f_cat = get_font("bold", 32)
    f_hook = get_font("black", 92)
    f_sub = get_font("medium", 40)
    f_chip_lbl = get_font("bold", 34)
    f_chip_val = get_font("extrabold", 34)

    # 5. Top Meta Header Bar (y: 75 - 170)
    day_str = f"DAY {day_num:02d} OF 100"
    dw = d.textlength(day_str, font=f_day)
    d.rounded_rectangle([90, 75, 90 + dw + 55, 155], radius=16, fill=(222, 90, 68))
    d.text((118, 95), day_str, font=f_day, fill=(255, 255, 255))

    d.text((90 + dw + 85, 100), "// THE FOUNDER'S WEB PLAYBOOK", font=f_meta, fill=(165, 185, 210))

    handle_str = "@extrovertnerd.dev ✓"
    hw = d.textlength(handle_str, font=f_handle)
    d.text((W - 90 - hw, 98), handle_str, font=f_handle, fill=(245, 158, 11))

    # Clean divider hairline
    d.line([(90, 185), (W - 90, 185)], fill=(255, 255, 255, 45), width=2)

    # 6. Category Tag Pill (y: 220)
    cat_str = f"⚡ {track.upper()} AUDIT"
    cw = d.textlength(cat_str, font=f_cat)
    d.rounded_rectangle([90, 220, 90 + cw + 45, 285], radius=12, fill=(16, 22, 34), outline=(45, 55, 75), width=2)
    d.text((112, 235), cat_str, font=f_cat, fill=(6, 182, 212))

    # 7. Giant Typographic Hook Lines (y: 320 - 580)
    title_text = day_data["title"]
    title_lines = wrap_text_to_lines(title_text, f_hook, max_width=W - 180, draw=d)[:3]

    ty = 320
    hl = day_data.get("highlight", "")

    for line in title_lines:
        if hl and hl in line:
            parts = line.split(hl)
            x_cursor = 90
            if parts[0]:
                d.text((x_cursor, ty), parts[0], font=f_hook, fill=(255, 255, 255))
                x_cursor += d.textlength(parts[0], font=f_hook)

            hl_w = d.textlength(hl, font=f_hook)
            d.rectangle([x_cursor - 8, ty + 2, x_cursor + hl_w + 16, ty + 96], fill=(222, 90, 68))
            d.text((x_cursor + 4, ty), hl, font=f_hook, fill=(255, 255, 255))
            x_cursor += hl_w + 16

            if len(parts) > 1 and parts[1]:
                d.text((x_cursor, ty), parts[1], font=f_hook, fill=(255, 255, 255))
        else:
            d.text((90, ty), line, font=f_hook, fill=(255, 255, 255))
        ty += 110

    # Sub-hook line
    subhook_text = day_data.get("subhook", "")
    d.text((90, ty + 12), subhook_text, font=f_sub, fill=(205, 220, 235))

    # 8. Floating Real-World Benchmark HUD (Over the Real Photo!)
    chip_y = ty + 85
    v_data = day_data.get("visual_data", {})
    badge_label = v_data.get("badge", "CORE WEB VITALS PASSED ✓")
    metric_quick = v_data.get("score", "99")

    chip_box = [90, chip_y, W - 90, chip_y + 115]
    d.rounded_rectangle(chip_box, radius=18, fill=(14, 18, 28), outline=(16, 185, 129), width=3)
    d.text((125, chip_y + 36), "⚡ LIVE BENCHMARK:", font=f_chip_lbl, fill=(16, 185, 129))
    d.text((540, chip_y + 34), f"{badge_label}  ·  SCORE: {metric_quick}", font=f_chip_val, fill=(255, 255, 255))

    # 9. 3 Actionable Glassmorphic Takeaway Cards (y: 1330 - 2000)
    takeaways = day_data.get("takeaways", [])
    f_num = get_font("black", 38)
    f_tt = get_font("bold", 42)
    f_td = get_font("medium", 34)

    colors_cycle = [(16, 185, 129), (6, 182, 212), (245, 158, 11)]
    ay = 1330

    for idx, (t_title, t_desc) in enumerate(takeaways[:3]):
        row_h = 200
        # Glassmorphic Dark Card
        d.rounded_rectangle([90, ay, W - 90, ay + row_h], radius=22, fill=(18, 24, 35), outline=(42, 52, 70), width=2)

        # Circular number badge
        col = colors_cycle[idx % len(colors_cycle)]
        d.rounded_rectangle([125, ay + 35, 225, ay + 135], radius=16, fill=col)
        d.text((148, ay + 55), f"0{idx+1}", font=f_num, fill=(10, 15, 22))

        # Title
        d.text((255, ay + 38), t_title, font=f_tt, fill=(255, 255, 255))

        # Description wrapped cleanly
        desc_lines = wrap_text_to_lines(t_desc, f_td, max_width=W - 380, draw=d)
        dy_line = ay + 98
        for dline in desc_lines[:2]:
            d.text((255, dy_line), dline, font=f_td, fill=(195, 210, 228))
            dy_line += 46

        ay += row_h + 22

    # 10. UPGRADED EXECUTIVE PROMOTION DECK (y: 2025 - 2635)
    pbox_y = 2025
    pbox_h = 610
    d.rounded_rectangle([90, pbox_y, W - 90, pbox_y + pbox_h], radius=28, fill=(14, 18, 28), outline=(222, 90, 68), width=4)

    # Brand Title Pill (strictly extrovertnerd, no Ravi Chauhan)
    f_brand_pill = get_font("extrabold", 30)
    brand_tag = "⚡ EXTROVERTNERD · WEB ENGINEERING & ARCHITECTURE"
    bt_w = d.textlength(brand_tag, font=f_brand_pill)
    d.rounded_rectangle([130, pbox_y + 35, 130 + bt_w + 50, pbox_y + 98], radius=14, fill=(245, 158, 11))
    d.text((155, pbox_y + 48), brand_tag, font=f_brand_pill, fill=(12, 16, 24))

    # Availability status
    f_status = get_font("bold", 30)
    status_tag = "🟢 ACCEPTING CLIENTS THIS MONTH"
    st_w = d.textlength(status_tag, font=f_status)
    d.rounded_rectangle([W - 130 - st_w - 50, pbox_y + 35, W - 130, pbox_y + 98], radius=14, fill=(20, 36, 30), outline=(16, 185, 129), width=2)
    d.text((W - 130 - st_w - 25, pbox_y + 48), status_tag, font=f_status, fill=(16, 185, 129))

    # High-Converting Hook Headline
    f_cta_head = get_font("black", 52)
    d.text((130, pbox_y + 125), "WANT A WEBSITE THAT ACTUALLY GENERATES LEADS?", font=f_cta_head, fill=(255, 255, 255))

    f_cta_sub = get_font("medium", 36)
    d.text((130, pbox_y + 195), "We engineer blazing-fast custom websites & automated internal software tools.", font=f_cta_sub, fill=(200, 215, 230))

    # 3 Guarantee micro-badges
    badges = ["✓ Sub-1s Load Speed", "✓ 100% Custom Code", "✓ Lead Generation UI"]
    f_badge = get_font("bold", 28)
    bx_curr = 130
    for b in badges:
        bw = d.textlength(b, font=f_badge)
        d.rounded_rectangle([bx_curr, pbox_y + 255, bx_curr + bw + 32, pbox_y + 305], radius=10, fill=(24, 32, 46))
        d.text((bx_curr + 16, pbox_y + 266), b, font=f_badge, fill=(16, 185, 129))
        bx_curr += int(bw + 45)

    # Contact Action Deck (Two Floating Cards)
    f_ct_lbl = get_font("bold", 30)
    f_ct_val = get_font("extrabold", 36)

    # DM Action Box (Left half)
    dm_w = 930
    d.rounded_rectangle([130, pbox_y + 330, 130 + dm_w, pbox_y + 435], radius=18, fill=(22, 28, 42), outline=(50, 65, 88), width=2)
    d.text((160, pbox_y + 355), '💬 DM "BUILD" on Instagram:', font=f_ct_lbl, fill=(200, 215, 230))
    d.text((160, pbox_y + 388), "@extrovertnerd.dev", font=f_ct_val, fill=(16, 185, 129))

    # Direct Email Box (Right half)
    em_x = 130 + dm_w + 30
    d.rounded_rectangle([em_x, pbox_y + 330, W - 130, pbox_y + 435], radius=18, fill=(22, 28, 42), outline=(50, 65, 88), width=2)
    d.text((em_x + 30, pbox_y + 355), "✉️ Direct Project Inquiries:", font=f_ct_lbl, fill=(200, 215, 230))
    d.text((em_x + 30, pbox_y + 388), "extrovertnerd.dev@gmail.com", font=f_ct_val, fill=(6, 182, 212))

    # Bottom CTA Banner
    f_btn = get_font("black", 36)
    btn_w = 880
    d.rounded_rectangle([130, pbox_y + 465, 130 + btn_w, pbox_y + 555], radius=16, fill=(16, 185, 129))
    d.text((165, pbox_y + 494), "🚀 DM FOR CUSTOM TOOLS & WEBSITES ↗", font=f_btn, fill=(10, 15, 22))

    f_bm = get_font("bold", 32)
    bm_str = "SAVE FOR YOUR NEXT BUILD 🔖"
    bm_w = d.textlength(bm_str, font=f_bm)
    d.text((W - 130 - bm_w, pbox_y + 498), bm_str, font=f_bm, fill=(245, 158, 11))

    # 11. Downsample from 2160x2700 to 1080x1350 for Retina Crispness
    final_img = canvas.resize((1080, 1350), Image.Resampling.LANCZOS)
    final_img.save(out_path, quality=95)
    print(f"✨ [poster_engine] Generated Day {day_num:02d} ({photo_key}) → {out_path}")

    # 12. Generate Instagram Post Caption
    caption_path = out_path.replace(".jpg", "_caption.txt")
    caption_content = generate_caption(day_data)
    with open(caption_path, "w", encoding="utf-8") as f:
        f.write(caption_content)

    return out_path


def generate_caption(day_data: dict) -> str:
    day = day_data["day"]
    title = day_data["title"]
    subhook = day_data.get("subhook", "")
    takeaways = day_data.get("takeaways", [])
    hashtags = day_data.get("hashtags", "#webdevelopment #websitetips")

    lines = [
        "DM for custom tools & websites 🚀",
        "━━━━━━━━━━━━━━━━━━━━━",
        f"DAY {day:02d} / 100: {title}",
        "",
        subhook,
        "",
        "Key takeaways to apply to your website today:",
        "",
    ]

    for t_title, t_desc in takeaways:
        lines.append(f"• {t_title}")
        lines.append(f"  {t_desc}")
        lines.append("")

    lines.extend([
        "━━━━━━━━━━━━━━━━━━━━━",
        "💼 NEED A HIGH-PERFORMANCE WEBSITE OR CUSTOM WEB TOOL?",
        "",
        "If you're running a business and want:",
        "✅ A blazing-fast, high-converting website",
        "✅ A custom internal software tool / automation dashboard",
        "✅ To eliminate manual spreadsheets and save 100+ hours every month",
        "",
        "📩 Send me a DM on Instagram: @extrovertnerd.dev (Type 'BUILD')",
        "📧 Or email directly: extrovertnerd.dev@gmail.com",
        "",
        "Let's build something exceptional for your business. 🚀",
        "",
        ".",
        ".",
        f"{hashtags} #extrovertnerd #webdevelopment #customtools #websitetips #buildinpublic #businessgrowth #techagency"
    ])

    return "\n".join(lines)
