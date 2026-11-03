"""
High-Converting Client Acquisition & Pitch Poster Engine for @extrovertnerd.dev.
Renders senior-agency-grade 4:5 Instagram posters designed specifically to convert
founders, business owners, and agencies into paying clients.
Resolution: 2160x2700 downsampled with Lanczos to 1080x1350.
"""

import os
from PIL import Image, ImageDraw, ImageOps
from poster_engine import (
    W, H, BASE_DIR, OUTPUT_DIR,
    get_font, wrap_text_to_lines, ensure_photo
)

def render_client_offer_poster(offer: dict, out_path: str = None) -> str:
    offer_id = offer.get("id", 1)
    if not out_path:
        out_path = os.path.join(OUTPUT_DIR, f"promo_offer_{offer_id:02d}.jpg")

    # 1. Resolve photo
    photo_key = offer.get("photo_key", "analytics_growth")
    photo_path = ensure_photo(photo_key)

    # 2. Base HD Photo
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

    # 3. Cinematic Gradients
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_ov = ImageDraw.Draw(overlay)

    # Top brand header shade
    for y in range(440):
        alpha = int(235 * (1 - (y / 440)))
        d_ov.line([(0, y), (W, y)], fill=(6, 8, 12, alpha))

    # Middle tint - photo glow
    for y in range(440, 1100):
        d_ov.line([(0, y), (W, y)], fill=(6, 8, 12, 55))

    # Deep bottom gradient for crisp text legibility
    for y in range(1100, H):
        progress = (y - 1100) / (H - 1100)
        alpha = int(255 * (progress ** 0.8))
        d_ov.line([(0, y), (W, y)], fill=(7, 9, 14, min(252, alpha)))

    canvas = Image.alpha_composite(bg, overlay).convert("RGB")
    d = ImageDraw.Draw(canvas)

    # 4. Typography Scale
    f_badge = get_font("black", 36)
    f_meta = get_font("bold", 34)
    f_handle = get_font("extrabold", 38)
    f_cat = get_font("bold", 32)
    f_hook = get_font("black", 92)
    f_sub = get_font("medium", 40)
    f_chip_lbl = get_font("bold", 34)
    f_chip_val = get_font("extrabold", 34)

    # 5. Top Header Bar
    badge_str = "🔥 CLIENT ACQUISITION"
    bw_pill = d.textlength(badge_str, font=f_badge)
    d.rounded_rectangle([90, 75, 90 + bw_pill + 55, 155], radius=16, fill=(234, 88, 12))  # Orange-red energy
    d.text((118, 95), badge_str, font=f_badge, fill=(255, 255, 255))

    d.text((90 + bw_pill + 85, 100), "// SCALE YOUR OPERATIONS", font=f_meta, fill=(165, 185, 210))

    handle_str = "@extrovertnerd.dev ✓"
    hw = d.textlength(handle_str, font=f_handle)
    d.text((W - 90 - hw, 98), handle_str, font=f_handle, fill=(245, 158, 11))

    d.line([(90, 185), (W - 90, 185)], fill=(255, 255, 255, 45), width=2)

    # 6. Category Tag Pill
    cat_str = f"⚡ {offer.get('badge', 'HIGH-CONVERTING WEB & TOOLS')}"
    cw = d.textlength(cat_str, font=f_cat)
    d.rounded_rectangle([90, 220, 90 + cw + 45, 285], radius=12, fill=(16, 22, 34), outline=(45, 55, 75), width=2)
    d.text((112, 235), cat_str, font=f_cat, fill=(6, 182, 212))

    # 7. Giant Typographic Hook
    title_text = offer["title"]
    title_lines = wrap_text_to_lines(title_text, f_hook, max_width=W - 180, draw=d)[:3]
    ty = 320
    hl = offer.get("highlight", "")

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

    # Subhook
    subhook_text = offer.get("subhook", "")
    d.text((90, ty + 12), subhook_text, font=f_sub, fill=(205, 220, 235))

    # 8. Floating Real-World ROI HUD
    chip_y = ty + 85
    m_badge = offer.get("metric_badge", "BENCHMARK")
    m_text = offer.get("metric_text", "GUARANTEED DELIVERY")

    d.rounded_rectangle([90, chip_y, W - 90, chip_y + 115], radius=18, fill=(14, 18, 28), outline=(16, 185, 129), width=3)
    d.text((125, chip_y + 36), f"📈 {m_badge}:", font=f_chip_lbl, fill=(16, 185, 129))
    d.text((580, chip_y + 34), m_text, font=f_chip_val, fill=(255, 255, 255))

    # 9. 3 Value Pillars
    pillars = offer.get("pillars", [])
    f_num = get_font("black", 38)
    f_tt = get_font("bold", 42)
    f_td = get_font("medium", 34)

    colors_cycle = [(16, 185, 129), (6, 182, 212), (245, 158, 11)]
    ay = 1330

    for idx, (p_title, p_desc) in enumerate(pillars[:3]):
        row_h = 200
        d.rounded_rectangle([90, ay, W - 90, ay + row_h], radius=22, fill=(18, 24, 35), outline=(42, 52, 70), width=2)

        col = colors_cycle[idx % len(colors_cycle)]
        d.rounded_rectangle([125, ay + 35, 225, ay + 135], radius=16, fill=col)
        d.text((148, ay + 55), f"0{idx+1}", font=f_num, fill=(10, 15, 22))

        d.text((255, ay + 38), p_title, font=f_tt, fill=(255, 255, 255))

        desc_lines = wrap_text_to_lines(p_desc, f_td, max_width=W - 380, draw=d)
        dy_line = ay + 98
        for dline in desc_lines[:2]:
            d.text((255, dy_line), dline, font=f_td, fill=(195, 210, 228))
            dy_line += 46

        ay += row_h + 22

    # 10. EXECUTIVE CLIENT CONVERSION DECK
    pbox_y = 2025
    pbox_h = 610
    d.rounded_rectangle([90, pbox_y, W - 90, pbox_y + pbox_h], radius=28, fill=(14, 18, 28), outline=(222, 90, 68), width=4)

    # Brand Title Pill
    f_brand_pill = get_font("extrabold", 30)
    brand_tag = "⚡ EXTROVERTNERD · WEB ENGINEERING & ARCHITECTURE"
    bt_w = d.textlength(brand_tag, font=f_brand_pill)
    d.rounded_rectangle([130, pbox_y + 35, 130 + bt_w + 50, pbox_y + 98], radius=14, fill=(245, 158, 11))
    d.text((155, pbox_y + 48), brand_tag, font=f_brand_pill, fill=(12, 16, 24))

    # Availability status
    f_status = get_font("bold", 30)
    status_tag = "🟢 ACCEPTING 2 CLIENTS THIS MONTH"
    st_w = d.textlength(status_tag, font=f_status)
    d.rounded_rectangle([W - 130 - st_w - 50, pbox_y + 35, W - 130, pbox_y + 98], radius=14, fill=(20, 36, 30), outline=(16, 185, 129), width=2)
    d.text((W - 130 - st_w - 25, pbox_y + 48), status_tag, font=f_status, fill=(16, 185, 129))

    # High-Converting Offer Headline
    f_cta_head = get_font("black", 50)
    offer_head = offer.get("offer_headline", "READY TO SCALE YOUR DIGITAL INFRASTRUCTURE?")
    d.text((130, pbox_y + 125), offer_head, font=f_cta_head, fill=(255, 255, 255))

    f_cta_sub = get_font("medium", 36)
    offer_sub = offer.get("offer_sub", "We engineer custom websites & automated tools that save hours and generate leads.")
    d.text((130, pbox_y + 195), offer_sub, font=f_cta_sub, fill=(200, 215, 230))

    # 3 Guarantee micro-badges
    badges = ["✓ 14-Day Delivery", "✓ 100% Custom Code", "✓ Fixed-Price Milestones"]
    f_badge_sub = get_font("bold", 28)
    bx_curr = 130
    for b in badges:
        bw = d.textlength(b, font=f_badge_sub)
        d.rounded_rectangle([bx_curr, pbox_y + 255, bx_curr + bw + 32, pbox_y + 305], radius=10, fill=(24, 32, 46))
        d.text((bx_curr + 16, pbox_y + 266), b, font=f_badge_sub, fill=(16, 185, 129))
        bx_curr += int(bw + 45)

    # Contact Action Deck (Two Floating Cards)
    f_ct_lbl = get_font("bold", 30)
    f_ct_val = get_font("extrabold", 36)
    keyword = offer.get("cta_keyword", "BUILD")

    # DM Action Box
    dm_w = 930
    d.rounded_rectangle([130, pbox_y + 330, 130 + dm_w, pbox_y + 435], radius=18, fill=(22, 28, 42), outline=(50, 65, 88), width=2)
    d.text((160, pbox_y + 355), f'💬 DM "{keyword}" on Instagram:', font=f_ct_lbl, fill=(200, 215, 230))
    d.text((160, pbox_y + 388), "@extrovertnerd.dev", font=f_ct_val, fill=(16, 185, 129))

    # Direct Email Box
    em_x = 130 + dm_w + 30
    d.rounded_rectangle([em_x, pbox_y + 330, W - 130, pbox_y + 435], radius=18, fill=(22, 28, 42), outline=(50, 65, 88), width=2)
    d.text((em_x + 30, pbox_y + 355), "✉️ Direct Project Inquiries:", font=f_ct_lbl, fill=(200, 215, 230))
    d.text((em_x + 30, pbox_y + 388), "extrovertnerd.dev@gmail.com", font=f_ct_val, fill=(6, 182, 212))

    # Bottom CTA Banner
    f_btn = get_font("black", 36)
    btn_text = offer.get("cta_button", f"🚀 DM '{keyword}' FOR CUSTOM TOOLS & WEBSITES ↗")
    btn_w = d.textlength(btn_text, font=f_btn) + 70
    btn_w = min(btn_w, 1050)
    d.rounded_rectangle([130, pbox_y + 465, 130 + btn_w, pbox_y + 555], radius=16, fill=(16, 185, 129))
    d.text((165, pbox_y + 494), btn_text, font=f_btn, fill=(10, 15, 22))

    f_bm = get_font("bold", 32)
    bm_str = "SAVE FOR YOUR NEXT BUILD 🔖"
    bm_w = d.textlength(bm_str, font=f_bm)
    d.text((W - 130 - bm_w, pbox_y + 498), bm_str, font=f_bm, fill=(245, 158, 11))

    # 11. Downsample for Retina Crispness
    final_img = canvas.resize((1080, 1350), Image.Resampling.LANCZOS)
    final_img.save(out_path, quality=95)
    print(f"✨ [client_promo_engine] Generated Offer {offer_id:02d} ({photo_key}) → {out_path}")

    # 12. Caption
    caption_path = out_path.replace(".jpg", "_caption.txt")
    caption_content = generate_client_offer_caption(offer)
    with open(caption_path, "w", encoding="utf-8") as f:
        f.write(caption_content)

    return out_path


def generate_client_offer_caption(offer: dict) -> str:
    title = offer["title"]
    subhook = offer.get("subhook", "")
    pillars = offer.get("pillars", [])
    keyword = offer.get("cta_keyword", "BUILD")
    hashtags = offer.get("hashtags", "#webdevelopment #businessgrowth #customtools")

    lines = [
        "DM for custom tools & websites 🚀",
        "━━━━━━━━━━━━━━━━━━━━━",
        f"💼 {title}",
        "",
        subhook,
        "",
        "Here is how we solve this for our clients:",
        "",
    ]

    for p_title, p_desc in pillars:
        lines.append(f"• {p_title}")
        lines.append(f"  {p_desc}")
        lines.append("")

    lines.extend([
        "━━━━━━━━━━━━━━━━━━━━━",
        "⚡ WANT TO WORK DIRECTLY WITH US THIS MONTH?",
        "",
        "We engineer high-performance web solutions for businesses:",
        "✅ Blazing-fast custom websites (Sub-1s speed, Next.js, no plugin bloat)",
        "✅ Custom internal tools & automation dashboards",
        "✅ 14-day turnaround with fixed milestones and zero hidden fees",
        "",
        f"📩 Send a DM on Instagram with the word '{keyword}' to @extrovertnerd.dev",
        "📧 Or email directly: extrovertnerd.dev@gmail.com",
        "",
        "We'll review your project and send you a custom proposal within 24 hours. 🚀",
        "",
        ".",
        ".",
        f"{hashtags} #extrovertnerd #webdeveloper #customtools #businessgrowth #techagency #buildinpublic"
    ])

    return "\n".join(lines)
