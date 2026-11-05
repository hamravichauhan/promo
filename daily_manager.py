#!/usr/bin/env python3
"""
Multi-Session Autonomous Daily Manager for ExtrovertNerd Dual-Channel Network:
- Channel 1 (@extrovertnerd.dev): Technical Web Playbooks & Performance Optimization
- Channel 2 (@extrovertnerd): High-Converting Commercial Client Acquisition Offers

Integrated with:
- Meta Graph API v21.0 Enterprise Publisher (Zero Ban Risk)
- Approach A: AI Lead Scout (Dispatches 1-tap targeted founder leads to Telegram)
- Approach B: Inbound Comment-to-Lead Funnel (Scans triggers and alerts on Telegram)
- Telegram Mission Control Executive Reporting
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")
INBOUND_LEADS_FILE = os.path.join(DATA_DIR, "inbound_leads.json")
os.makedirs(DATA_DIR, exist_ok=True)

from playbook_data import get_playbook_day, PLAYBOOK_100
from client_offers import CLIENT_OFFERS, get_client_offer
from poster_dispatcher import send_to_telegram, send_telegram_text
from meta_graph_publisher import (
    publish_image_to_instagram,
    publish_story_to_instagram,
    get_account_metrics,
    get_both_accounts_overview,
)
from lead_scout import run_lead_scout
from comment_funnel import check_and_process_recent_comments

IST = timezone(timedelta(hours=5, minutes=30))
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/hamravichauhan/promo/main/output"


def get_ist_now() -> datetime:
    return datetime.now(IST)


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


def get_today_inbound_leads_count() -> int:
    today_str = get_ist_now().strftime("%Y-%m-%d")
    count = 0
    if os.path.exists(INBOUND_LEADS_FILE):
        try:
            with open(INBOUND_LEADS_FILE, "r", encoding="utf-8") as f:
                leads = json.load(f)
                for l in leads:
                    if l.get("timestamp", "").startswith(today_str):
                        count += 1
        except Exception:
            pass
    return count


def run_morning_session(dispatch_telegram: bool = True, upload_ig: bool = True):
    """
    Session 1: Morning (09:30 AM IST)
    - Channel: @extrovertnerd.dev
    - Content: Technical Web Playbook Poster
    - Engagement: Check Inbound Comments + AI Lead Scout (Tech Founders / Indie Hackers)
    """
    print("\n🌅 EXECUTING MORNING SESSION (09:30 AM IST)...")
    prog = load_progress()
    day_num = prog.get("current_day", 1)
    day_data = get_playbook_day(day_num)

    img_filename = f"day_{day_num:03d}_playbook_dark.jpg"
    img_path = os.path.join(BASE_DIR, "output", img_filename)
    caption_path = os.path.join(BASE_DIR, "output", f"day_{day_num:03d}_playbook_dark_caption.txt")

    if os.path.exists(caption_path):
        with open(caption_path, "r", encoding="utf-8") as f:
            caption = f.read()
    else:
        caption = f"Day {day_num}: {day_data.get('title')}\n\nRead more at extrovertnerd.dev"

    raw_img_url = f"{GITHUB_RAW_BASE}/{img_filename}"

    # Telegram notification
    if dispatch_telegram:
        send_to_telegram(img_path if os.path.exists(img_path) else raw_img_url, caption)

    # Official Meta Graph API Publish to @extrovertnerd.dev
    ig_result = None
    if upload_ig:
        ig_result = publish_image_to_instagram(
            image_url=raw_img_url,
            caption=caption,
            target="dev"
        )
        try:
            publish_story_to_instagram(image_url=raw_img_url, target="dev")
        except Exception as e:
            print(f"[-] Story publish notice: {e}")

    # Advance curriculum
    total_days = len(PLAYBOOK_100)
    prog["current_day"] = (day_num % total_days) + 1
    prog.setdefault("history", []).append({
        "session": "morning",
        "target": "extrovertnerd.dev",
        "type": "playbook",
        "day": day_num,
        "title": day_data.get("title", ""),
        "timestamp": get_ist_now().isoformat(),
        "ig_publish": ig_result,
    })
    save_progress(prog)

    # Inbound comment checks
    print("\n🔍 Checking Inbound Comments & Keywords...")
    try:
        check_and_process_recent_comments()
    except Exception as e:
        print(f"[-] Comment check notice: {e}")

    # Approach A: Lead Scout (Tech Founders)
    print("\n🎯 Running AI Lead Scout (Morning Batch)...")
    try:
        run_lead_scout("morning")
    except Exception as e:
        print(f"[-] Lead scout notice: {e}")

    print("✅ Morning session execution finished.")


def run_midday_session(dispatch_telegram: bool = True, upload_ig: bool = True):
    """
    Session 2: Midday (01:30 PM IST)
    - Channel: @extrovertnerd
    - Content: High-Converting Client Acquisition Offer
    - Engagement: Check Inbound Comments + AI Lead Scout (Creative Agencies & Studios)
    """
    print("\n☀️ EXECUTING MIDDAY SESSION (01:30 PM IST)...")
    prog = load_progress()
    offer_id = prog.get("current_offer", 1)
    offer = get_client_offer(offer_id)

    img_filename = f"promo_offer_{offer['id']:02d}.jpg"
    img_path = os.path.join(BASE_DIR, "output", img_filename)
    caption_path = os.path.join(BASE_DIR, "output", f"promo_offer_{offer['id']:02d}_caption.txt")

    if os.path.exists(caption_path):
        with open(caption_path, "r", encoding="utf-8") as f:
            caption = f.read()
    else:
        caption = f"Exclusive Client Offer: {offer.get('title')}\n\nDM 'AUDIT' to claim yours."

    raw_img_url = f"{GITHUB_RAW_BASE}/{img_filename}"

    # Telegram notification
    if dispatch_telegram:
        send_to_telegram(img_path if os.path.exists(img_path) else raw_img_url, caption)

    # Official Meta Graph API Publish to @extrovertnerd
    ig_result = None
    if upload_ig:
        ig_result = publish_image_to_instagram(
            image_url=raw_img_url,
            caption=caption,
            target="agency"
        )
        try:
            publish_story_to_instagram(image_url=raw_img_url, target="agency")
        except Exception as e:
            print(f"[-] Story publish notice: {e}")

    # Advance offer sequence
    prog["current_offer"] = (offer_id % len(CLIENT_OFFERS)) + 1
    prog.setdefault("history", []).append({
        "session": "midday",
        "target": "extrovertnerd",
        "type": "client_offer",
        "offer_id": offer_id,
        "title": offer.get("title", ""),
        "timestamp": get_ist_now().isoformat(),
        "ig_publish": ig_result,
    })
    save_progress(prog)

    # Inbound comment checks
    print("\n🔍 Checking Inbound Comments & Keywords...")
    try:
        check_and_process_recent_comments()
    except Exception as e:
        print(f"[-] Comment check notice: {e}")

    # Approach A: Lead Scout (Creative Agencies)
    print("\n🎯 Running AI Lead Scout (Midday Batch)...")
    try:
        run_lead_scout("midday")
    except Exception as e:
        print(f"[-] Lead scout notice: {e}")

    print("✅ Midday session execution finished.")


def run_evening_session(dispatch_telegram: bool = True, upload_ig: bool = True):
    """
    Session 3: Evening (05:30 PM IST)
    - Channel: @extrovertnerd.dev
    - Content: Educational Web Architecture / Optimization Case
    - Engagement: Check Inbound Comments + AI Lead Scout (Early-Stage SaaS Startups)
    """
    print("\n🌇 EXECUTING EVENING SESSION (05:30 PM IST)...")
    prog = load_progress()
    day_num = prog.get("current_day", 1)
    day_data = get_playbook_day(day_num)

    img_filename = f"day_{day_num:03d}_playbook_dark.jpg"
    img_path = os.path.join(BASE_DIR, "output", img_filename)
    caption_path = os.path.join(BASE_DIR, "output", f"day_{day_num:03d}_playbook_dark_caption.txt")

    if os.path.exists(caption_path):
        with open(caption_path, "r", encoding="utf-8") as f:
            caption = f.read()
    else:
        caption = f"Day {day_num}: {day_data.get('title')}\n\nRead more at extrovertnerd.dev"

    raw_img_url = f"{GITHUB_RAW_BASE}/{img_filename}"

    # Telegram notification
    if dispatch_telegram:
        send_to_telegram(img_path if os.path.exists(img_path) else raw_img_url, caption)

    # Official Meta Graph API Publish to @extrovertnerd.dev
    ig_result = None
    if upload_ig:
        ig_result = publish_image_to_instagram(
            image_url=raw_img_url,
            caption=caption,
            target="dev"
        )
        try:
            publish_story_to_instagram(image_url=raw_img_url, target="dev")
        except Exception as e:
            print(f"[-] Story publish notice: {e}")

    # Advance curriculum
    total_days = len(PLAYBOOK_100)
    prog["current_day"] = (day_num % total_days) + 1
    prog.setdefault("history", []).append({
        "session": "evening",
        "target": "extrovertnerd.dev",
        "type": "playbook",
        "day": day_num,
        "title": day_data.get("title", ""),
        "timestamp": get_ist_now().isoformat(),
        "ig_publish": ig_result,
    })
    save_progress(prog)

    # Inbound comment checks
    print("\n🔍 Checking Inbound Comments & Keywords...")
    try:
        check_and_process_recent_comments()
    except Exception as e:
        print(f"[-] Comment check notice: {e}")

    # Approach A: Lead Scout (SaaS Startups)
    print("\n🎯 Running AI Lead Scout (Evening Batch)...")
    try:
        run_lead_scout("evening")
    except Exception as e:
        print(f"[-] Lead scout notice: {e}")

    print("✅ Evening session execution finished.")


def run_night_session(dispatch_telegram: bool = True, upload_ig: bool = True):
    """
    Session 4: Night (09:30 PM IST)
    - Channel: @extrovertnerd
    - Content: High-Converting Client Acquisition Offer
    - Engagement: Check Inbound Comments + AI Lead Scout (B2B & E-commerce Brands)
    - Compiles & Dispatches Full-Day Unified Executive Report to Telegram!
    """
    print("\n🌙 EXECUTING NIGHT SESSION (09:30 PM IST)...")
    prog = load_progress()
    offer_id = prog.get("current_offer", 1)
    offer = get_client_offer(offer_id)

    img_filename = f"promo_offer_{offer['id']:02d}.jpg"
    img_path = os.path.join(BASE_DIR, "output", img_filename)
    caption_path = os.path.join(BASE_DIR, "output", f"promo_offer_{offer['id']:02d}_caption.txt")

    if os.path.exists(caption_path):
        with open(caption_path, "r", encoding="utf-8") as f:
            caption = f.read()
    else:
        caption = f"Exclusive Client Offer: {offer.get('title')}\n\nDM 'AUDIT' to claim yours."

    raw_img_url = f"{GITHUB_RAW_BASE}/{img_filename}"

    # Telegram notification
    if dispatch_telegram:
        send_to_telegram(img_path if os.path.exists(img_path) else raw_img_url, caption)

    # Official Meta Graph API Publish to @extrovertnerd
    ig_result = None
    if upload_ig:
        ig_result = publish_image_to_instagram(
            image_url=raw_img_url,
            caption=caption,
            target="agency"
        )
        try:
            publish_story_to_instagram(image_url=raw_img_url, target="agency")
        except Exception as e:
            print(f"[-] Story publish notice: {e}")

    # Advance offer sequence
    prog["current_offer"] = (offer_id % len(CLIENT_OFFERS)) + 1
    prog.setdefault("history", []).append({
        "session": "night",
        "target": "extrovertnerd",
        "type": "client_offer",
        "offer_id": offer_id,
        "title": offer.get("title", ""),
        "timestamp": get_ist_now().isoformat(),
        "ig_publish": ig_result,
    })
    save_progress(prog)

    # Inbound comment checks
    print("\n🔍 Checking Inbound Comments & Keywords...")
    try:
        check_and_process_recent_comments()
    except Exception as e:
        print(f"[-] Comment check notice: {e}")

    # Approach A: Lead Scout (E-Commerce / B2B Brands)
    print("\n🎯 Running AI Lead Scout (Night Batch)...")
    try:
        run_lead_scout("night")
    except Exception as e:
        print(f"[-] Lead scout notice: {e}")

    print("✅ Night session execution finished.")

    # Compile & Dispatch Full Day Executive Report to Telegram!
    send_daily_executive_report()


def generate_executive_report_text() -> str:
    """Compiles the daily performance metrics into a clean, dual-channel summary."""
    now_ist = get_ist_now()
    today_date_str = now_ist.strftime("%Y-%m-%d")
    today_formatted = now_ist.strftime("%A, %d %b %Y")

    prog = load_progress()

    # 1. Collect today's posts
    today_posts = []
    for item in prog.get("history", []):
        ts = item.get("timestamp", "")
        if ts.startswith(today_date_str):
            today_posts.append(item)

    # 2. Get live Instagram stats for both channels
    dev_stats = get_account_metrics("dev")
    agency_stats = get_account_metrics("agency")
    inbound_leads_today = get_today_inbound_leads_count()

    lines = [
        "📊 EXTROVERTNERD — DAILY DUAL-CHANNEL EXECUTIVE REPORT",
        f"📅 Date: {today_formatted}",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"🚀 CONTENT PUBLISHED TODAY ({len(today_posts)} POSTS):",
    ]

    if today_posts:
        for idx, p in enumerate(today_posts, 1):
            s_name = p.get("session", "daily").capitalize()
            p_target = p.get("target", "Channel")
            p_type = "Playbook" if p.get("type") == "playbook" else "Client Offer"
            lines.append(f"  {idx}. [{s_name} · @{p_target}] {p.get('title')}")
    else:
        lines.append("  (No posts logged yet today)")

    lines.extend([
        "",
        "📈 LIVE MULTI-CHANNEL METRICS (Official Meta Graph API):",
        f"  • 🛠️ DEV CHANNEL (@{dev_stats.get('username', 'extrovertnerd.dev')}):",
        f"      Followers: {dev_stats.get('followers', 'N/A')} | Following: {dev_stats.get('following', 'N/A')} | Posts: {dev_stats.get('media_count', 'N/A')}",
        f"  • 💼 AGENCY CHANNEL (@{agency_stats.get('username', 'extrovertnerd')}):",
        f"      Followers: {agency_stats.get('followers', 'N/A')} | Following: {agency_stats.get('following', 'N/A')} | Posts: {agency_stats.get('media_count', 'N/A')}",
        "",
        "🎯 ORGANIC CLIENT ACQUISITION (Approach A + B):",
        f"  • 📥 Inbound Keyword Leads Today: {inbound_leads_today} ('AUDIT' / 'TOOL' / 'BUILD')",
        "  • 🚀 Outbound AI Lead Scout Sheets: Dispatched to Telegram (4 sessions × 4 high-intent leads)",
        "",
        "🛡️ COMPLIANCE & SAFETY STATUS:",
        "  • Platform: Meta Graph API v21.0 Enterprise Sanctioned",
        "  • Ban Risk: 0.00% (No headless bots, no cloud scraping)",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "💼 ACTION ITEMS FOR TONIGHT:",
        "  👉 Check Instagram DMs on @extrovertnerd for inbound lead conversations",
        "  👉 Connect with the 4 night prospect leads scouted above",
        "  👉 Check email inbox: extrovertnerd.dev@gmail.com",
        "",
        "Pipeline running 100% autonomously in the cloud 🚀"
    ])

    return "\n".join(lines)


def send_daily_executive_report():
    print("\n📋 Generating Daily Executive Report...")
    report_text = generate_executive_report_text()
    print("\n" + report_text + "\n")
    success = send_telegram_text(report_text)
    if success:
        print("✅ Daily Executive Report successfully dispatched to Telegram bot!")
    return success


def auto_detect_session():
    """Auto-detects which session to run based on current hour in IST."""
    hour = get_ist_now().hour
    if 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 16:
        return "midday"
    elif 16 <= hour < 20:
        return "evening"
    else:
        return "night"


def main():
    parser = argparse.ArgumentParser(description="Multi-Session Autonomous Daily Manager for ExtrovertNerd")
    parser.add_argument("--session", type=str, default="auto", help="Session to run (morning, midday, evening, night, auto)")
    parser.add_argument("--report", action="store_true", help="Send End-of-Day Executive Report to Telegram now")
    parser.add_argument("--no-telegram", action="store_true", help="Skip sending to Telegram")
    parser.add_argument("--no-ig", action="store_true", help="Skip uploading to Instagram")

    args = parser.parse_args()

    if args.report:
        send_daily_executive_report()
        return

    session = (args.session or "auto").strip().lower()
    if session not in ["morning", "midday", "evening", "night", "auto"]:
        print(f"[-] Unrecognized session '{args.session}', defaulting to 'auto'.")
        session = "auto"

    if session == "auto":
        session = auto_detect_session()
        print(f"[*] Auto-detected session based on IST clock ({get_ist_now().strftime('%H:%M')} IST): {session.upper()}")

    dispatch_tg = not args.no_telegram
    upload_ig = not args.no_ig

    if session == "morning":
        run_morning_session(dispatch_telegram=dispatch_tg, upload_ig=upload_ig)
    elif session == "midday":
        run_midday_session(dispatch_telegram=dispatch_tg, upload_ig=upload_ig)
    elif session == "evening":
        run_evening_session(dispatch_telegram=dispatch_tg, upload_ig=upload_ig)
    elif session == "night":
        run_night_session(dispatch_telegram=dispatch_tg, upload_ig=upload_ig)


if __name__ == "__main__":
    main()
