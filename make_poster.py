#!/usr/bin/env python3
"""
100-Day Web Playbook & Client Acquisition Lead-Gen Engine.
Renders senior-agency-grade 4:5 Instagram posters + formatted captions.
Supports 1-click dispatch to Telegram, direct Instagram publishing,
dedicated client acquisition offers, and autonomous organic follower growth.
"""

import os
import sys
import json
import random
import argparse
from datetime import datetime

# Pillow 10+ compatibility shim
import PIL.Image
if not hasattr(PIL.Image, "ANTIALIAS"):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

from playbook_data import PLAYBOOK_100, get_playbook_day
from poster_engine import render_poster
from poster_dispatcher import send_to_telegram, upload_to_instagram
from client_offers import CLIENT_OFFERS, get_client_offer
from client_promo_engine import render_client_offer_poster


def load_progress() -> dict:
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"current_day": 1, "current_offer": 1, "history": []}


def save_progress(prog: dict):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(prog, f, indent=2)


def generate_single_poster(
    day_num: int,
    theme: str = "dark",
    dispatch_telegram: bool = False,
    dispatch_instagram: bool = False,
) -> dict:
    day_data = get_playbook_day(day_num)

    print("\n" + "=" * 65)
    print(f"🚀 GENERATING PLAYBOOK POSTER: DAY {day_data['day']:02d} / 100")
    print(f"📌 Track     : {day_data.get('track', 'Web Optimization')}")
    print(f"🎯 Headline  : {day_data['title']}")
    print(f"🎨 Theme     : {theme.upper()} MODE")
    print("=" * 65 + "\n")

    out_filename = f"day_{day_data['day']:03d}_playbook_{theme}.jpg"
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    rendered_image = render_poster(day_data, theme_name=theme, out_path=out_path)

    caption_path = rendered_image.replace(".jpg", "_caption.txt")
    with open(caption_path, "r", encoding="utf-8") as f:
        caption_text = f.read()

    print(f"✅ Poster Generated  : {rendered_image}")
    print(f"📝 Caption Generated : {caption_path}\n")

    if dispatch_telegram:
        send_to_telegram(rendered_image, caption_text)

    if dispatch_instagram:
        upload_to_instagram(rendered_image, caption_text)

    prog = load_progress()
    prog["history"].append({
        "type": "curriculum",
        "day": day_num,
        "title": day_data["title"],
        "timestamp": datetime.now().isoformat(),
        "image": rendered_image,
        "telegram_sent": dispatch_telegram,
        "instagram_uploaded": dispatch_instagram,
    })
    save_progress(prog)

    return {
        "day": day_num,
        "image_path": rendered_image,
        "caption_path": caption_path,
        "title": day_data["title"],
    }


def generate_client_promo_poster(
    offer_id: int = 1,
    dispatch_telegram: bool = False,
    dispatch_instagram: bool = False,
) -> dict:
    offer = get_client_offer(offer_id)

    print("\n" + "=" * 65)
    print(f"💼 GENERATING CLIENT ACQUISITION OFFER #{offer['id']}")
    print(f"🎯 Offer     : {offer['title']}")
    print(f"🏷️ Badge     : {offer.get('badge')}")
    print(f"💬 CTA Word  : DM '{offer.get('cta_keyword')}'")
    print("=" * 65 + "\n")

    out_filename = f"promo_offer_{offer['id']:02d}.jpg"
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    rendered_image = render_client_offer_poster(offer, out_path=out_path)

    caption_path = rendered_image.replace(".jpg", "_caption.txt")
    with open(caption_path, "r", encoding="utf-8") as f:
        caption_text = f.read()

    print(f"✅ Client Offer Poster : {rendered_image}")
    print(f"📝 Caption File        : {caption_path}\n")

    if dispatch_telegram:
        send_to_telegram(rendered_image, caption_text)

    if dispatch_instagram:
        upload_to_instagram(rendered_image, caption_text)

    prog = load_progress()
    prog["history"].append({
        "type": "client_offer",
        "offer_id": offer_id,
        "title": offer["title"],
        "timestamp": datetime.now().isoformat(),
        "image": rendered_image,
        "telegram_sent": dispatch_telegram,
        "instagram_uploaded": dispatch_instagram,
    })
    save_progress(prog)

    return {
        "offer_id": offer_id,
        "image_path": rendered_image,
        "caption_path": caption_path,
        "title": offer["title"],
    }


def run_growth_cycle():
    """Runs autonomous, safe organic engagement to grow the account."""
    try:
        from growth_engine import init_client, safe_engage_leads, TARGET_HASHTAGS
        cl = init_client()
        tag = random.choice(TARGET_HASHTAGS)
        safe_engage_leads(cl, tag, max_follows=10, max_likes=12)
    except Exception as e:
        print(f"[-] Growth cycle exception: {e}")


def main():
    parser = argparse.ArgumentParser(description="100-Day Web Playbook & Client Acquisition Lead Engine")
    parser.add_argument("--day", type=int, default=None, help="Specific day number (1 to 100)")
    parser.add_argument("--today", action="store_true", help="Automatically generate and advance today's daily poster")
    parser.add_argument("--offer", type=int, default=None, help="Generate specific client acquisition offer poster (1 to 8+)")
    parser.add_argument("--promo", action="store_true", help="Generate today's client pitch/acquisition poster")
    parser.add_argument("--grow", action="store_true", help="Run safe organic growth cycle (story viewing, targeted follows & likes)")
    parser.add_argument("--theme", type=str, default="dark", choices=["dark", "light"], help="Design aesthetic theme")
    parser.add_argument("--send-telegram", action="store_true", help="Send rendered poster + caption to Telegram bot")
    parser.add_argument("--upload-ig", action="store_true", help="Publish poster + caption directly to Instagram")
    parser.add_argument("--all", action="store_true", help="Batch render all 100 days of posters into output/")
    parser.add_argument("--list", action="store_true", help="List all 100 topics across the 8 curriculum tracks")

    args = parser.parse_args()

    # List mode
    if args.list:
        print("\n" + "=" * 70)
        print("📚 100-DAY WEB DEVELOPMENT & CLIENT ACQUISITION PLAYBOOK")
        print("=" * 70)
        for d in range(1, 101):
            info = get_playbook_day(d)
            print(f"  Day {d:02d} [{info.get('track', 'GENERAL')}]: {info['title']}")
        print("\n" + "=" * 70)
        print("💼 CLIENT ACQUISITION OFFER POSTERS")
        print("=" * 70)
        for off in CLIENT_OFFERS:
            print(f"  Offer #{off['id']:02d} [{off.get('badge')}]: {off['title']} (DM '{off['cta_keyword']}')")
        print()
        return

    # Specific client acquisition offer
    if args.offer is not None:
        generate_client_promo_poster(
            offer_id=args.offer,
            dispatch_telegram=args.send_telegram,
            dispatch_instagram=args.upload_ig
        )
        if args.grow:
            run_growth_cycle()
        return

    # Client promo mode (uses current offer in queue)
    if args.promo:
        prog = load_progress()
        current_off = prog.get("current_offer", 1)
        generate_client_promo_poster(
            offer_id=current_off,
            dispatch_telegram=args.send_telegram,
            dispatch_instagram=args.upload_ig
        )
        prog["current_offer"] = (current_off % len(CLIENT_OFFERS)) + 1
        save_progress(prog)
        if args.grow:
            run_growth_cycle()
        return

    # Batch generate all mode
    if args.all:
        print(f"\n🚀 Batch rendering all 100 playbook posters ({args.theme} mode)...")
        for d in range(1, 101):
            day_data = get_playbook_day(d)
            out_filename = f"day_{d:03d}_playbook_{args.theme}.jpg"
            out_path = os.path.join(OUTPUT_DIR, out_filename)
            render_poster(day_data, theme_name=args.theme, out_path=out_path)

        print("\n💼 Batch rendering all Client Acquisition Offer posters...")
        for off in CLIENT_OFFERS:
            out_filename = f"promo_offer_{off['id']:02d}.jpg"
            out_path = os.path.join(OUTPUT_DIR, out_filename)
            render_client_offer_poster(off, out_path=out_path)

        print(f"\n✅ All posters rendered successfully into {OUTPUT_DIR}!\n")
        return

    # Today auto-advancement mode
    if args.today:
        prog = load_progress()
        target_day = prog.get("current_day", 1)
        generate_single_poster(
            day_num=target_day,
            theme=args.theme,
            dispatch_telegram=args.send_telegram,
            dispatch_instagram=args.upload_ig,
        )
        prog["current_day"] = min(100, target_day + 1)
        save_progress(prog)
        print(f"👉 Tomorrow's queue is set to Day {prog['current_day']:02d} / 100.\n")

        # Run growth cycle if requested
        if args.grow:
            print("🌱 Initiating automatic daily organic follower growth cycle...")
            run_growth_cycle()
        return

    # Specific day mode (defaults to Day 1)
    target_day = args.day if args.day is not None else 1
    generate_single_poster(
        day_num=target_day,
        theme=args.theme,
        dispatch_telegram=args.send_telegram,
        dispatch_instagram=args.upload_ig,
    )

    if args.grow:
        run_growth_cycle()


if __name__ == "__main__":
    main()
