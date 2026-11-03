#!/usr/bin/env python3
"""
Multi-Session Daily Manager for @extrovertnerd.dev.
Coordinates 3-4 daily publications (Web Playbooks + Client Acquisition Offers),
spreads out organic engagement (story views, likes, follows) naturally throughout the day,
and compiles & dispatches a comprehensive End-of-Day Executive Summary to Telegram.
"""

import os
import sys
import json
import time
import random
import argparse
from datetime import datetime, timezone, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")
GROWTH_DB_FILE = os.path.join(DATA_DIR, "growth_state.json")

from playbook_data import get_playbook_day
from client_offers import CLIENT_OFFERS, get_client_offer
from poster_engine import render_poster
from client_promo_engine import render_client_offer_poster
from poster_dispatcher import send_to_telegram, upload_to_instagram, send_telegram_text
from growth_engine import (
    init_client, safe_engage_leads, view_stories_for_users,
    load_growth_db, check_daily_limits, TARGET_HASHTAGS,
    get_optimized_hashtag, sync_follow_backs_and_analyze
)
from dm_autoresponder import check_and_reply_inbox

IST = timezone(timedelta(hours=5, minutes=30))


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


def run_morning_session(dispatch_telegram=True, upload_ig=True):
    """
    Session 1: Morning (09:30 AM IST)
    - Publishes: High-Impact Web Playbook Poster
    - Engagement: 4-5 targeted follows + 6 likes + 15 story views
    """
    print("\n🌅 EXECUTING MORNING SESSION (09:30 AM IST)...")
    prog = load_progress()
    day_num = prog.get("current_day", 1)
    day_data = get_playbook_day(day_num)

    out_file = os.path.join(BASE_DIR, "output", f"day_{day_num:03d}_playbook_dark.jpg")
    img_path = render_poster(day_data, theme_name="dark", out_path=out_file)
    caption_path = img_path.replace(".jpg", "_caption.txt")
    with open(caption_path, "r", encoding="utf-8") as f:
        caption = f.read()

    if dispatch_telegram:
        send_to_telegram(img_path, caption)
    if upload_ig:
        upload_to_instagram(img_path, caption)

    prog["current_day"] = min(100, day_num + 1)
    prog["history"].append({
        "session": "morning",
        "type": "playbook",
        "day": day_num,
        "title": day_data["title"],
        "timestamp": get_ist_now().isoformat(),
    })
    save_progress(prog)

    # Micro growth session
    print("🌱 Running Morning Lead Engagement & Inbox Check...")
    try:
        cl = init_client()
        check_and_reply_inbox(cl)
        tag = random.choice(["buildinpublic", "indiehackers", "techfounder"])
        safe_engage_leads(cl, tag, max_follows=4, max_likes=6)
    except Exception as e:
        print(f"[-] Growth notice: {e}")


def run_midday_session(dispatch_telegram=True, upload_ig=True):
    """
    Session 2: Midday (01:30 PM IST)
    - Publishes: High-Converting Client Acquisition Offer (DM 'AUDIT' / 'TOOL' / 'BUILD')
    - Engagement: Story Viewing Blitz (25 stories) + 4-5 targeted follows
    """
    print("\n☀️ EXECUTING MIDDAY SESSION (01:30 PM IST)...")
    prog = load_progress()
    offer_id = prog.get("current_offer", 1)
    offer = get_client_offer(offer_id)

    out_file = os.path.join(BASE_DIR, "output", f"promo_offer_{offer['id']:02d}.jpg")
    img_path = render_client_offer_poster(offer, out_path=out_file)
    caption_path = img_path.replace(".jpg", "_caption.txt")
    with open(caption_path, "r", encoding="utf-8") as f:
        caption = f.read()

    if dispatch_telegram:
        send_to_telegram(img_path, caption)
    if upload_ig:
        upload_to_instagram(img_path, caption)

    prog["current_offer"] = (offer_id % len(CLIENT_OFFERS)) + 1
    prog["history"].append({
        "session": "midday",
        "type": "client_offer",
        "offer_id": offer_id,
        "title": offer["title"],
        "timestamp": get_ist_now().isoformat(),
    })
    save_progress(prog)

    # Micro growth session
    print("🌱 Running Midday Lead Engagement & Inbox Check...")
    try:
        cl = init_client()
        check_and_reply_inbox(cl)
        tag = random.choice(["smallbusinessowner", "ecommercebusiness", "shopifydropshipping"])
        safe_engage_leads(cl, tag, max_follows=4, max_likes=6)
    except Exception as e:
        print(f"[-] Growth notice: {e}")


def run_evening_session(dispatch_telegram=True, upload_ig=True):
    """
    Session 3: Evening (05:30 PM IST)
    - Publishes: Educational Web Architecture / Optimization Case
    - Engagement: 4-5 targeted follows + 6 likes + 15 story views
    """
    print("\n🌇 EXECUTING EVENING SESSION (05:30 PM IST)...")
    prog = load_progress()
    day_num = prog.get("current_day", 1)
    day_data = get_playbook_day(day_num)

    out_file = os.path.join(BASE_DIR, "output", f"day_{day_num:03d}_playbook_dark.jpg")
    img_path = render_poster(day_data, theme_name="dark", out_path=out_file)
    caption_path = img_path.replace(".jpg", "_caption.txt")
    with open(caption_path, "r", encoding="utf-8") as f:
        caption = f.read()

    if dispatch_telegram:
        send_to_telegram(img_path, caption)
    if upload_ig:
        upload_to_instagram(img_path, caption)

    prog["current_day"] = min(100, day_num + 1)
    prog["history"].append({
        "session": "evening",
        "type": "playbook",
        "day": day_num,
        "title": day_data["title"],
        "timestamp": get_ist_now().isoformat(),
    })
    save_progress(prog)

    # Micro growth session
    print("🌱 Running Evening Lead Engagement & Inbox Check...")
    try:
        cl = init_client()
        check_and_reply_inbox(cl)
        tag = random.choice(["digitalagency", "saasstartup", "solopreneur"])
        safe_engage_leads(cl, tag, max_follows=4, max_likes=6)
    except Exception as e:
        print(f"[-] Growth notice: {e}")


def run_night_session(dispatch_telegram=True, upload_ig=True):
    """
    Session 4: Night (09:30 PM IST)
    - Publishes: High-Converting Client Acquisition Offer
    - Engagement: Final micro growth
    - Compiles & Sends Full-Day Executive Report to Telegram!
    """
    print("\n🌙 EXECUTING NIGHT SESSION (09:30 PM IST)...")
    prog = load_progress()
    offer_id = prog.get("current_offer", 1)
    offer = get_client_offer(offer_id)

    out_file = os.path.join(BASE_DIR, "output", f"promo_offer_{offer['id']:02d}.jpg")
    img_path = render_client_offer_poster(offer, out_path=out_file)
    caption_path = img_path.replace(".jpg", "_caption.txt")
    with open(caption_path, "r", encoding="utf-8") as f:
        caption = f.read()

    if dispatch_telegram:
        send_to_telegram(img_path, caption)
    if upload_ig:
        upload_to_instagram(img_path, caption)

    prog["current_offer"] = (offer_id % len(CLIENT_OFFERS)) + 1
    prog["history"].append({
        "session": "night",
        "type": "client_offer",
        "offer_id": offer_id,
        "title": offer["title"],
        "timestamp": get_ist_now().isoformat(),
    })
    save_progress(prog)

    # Micro growth session
    print("🌱 Running Night Lead Engagement & Inbox Check...")
    try:
        cl = init_client()
        check_and_reply_inbox(cl)
        tag = random.choice(["startuplife", "buildinpublic", "growthhacking"])
        safe_engage_leads(cl, tag, max_follows=4, max_likes=6)
    except Exception as e:
        print(f"[-] Growth notice: {e}")

    # Compile & Dispatch Full Day Executive Report to Telegram!
    send_daily_executive_report()


def generate_executive_report_text() -> str:
    """Compiles the daily performance metrics into a clean, professional summary."""
    now_ist = get_ist_now()
    today_date_str = now_ist.strftime("%Y-%m-%d")
    today_formatted = now_ist.strftime("%A, %d %b %Y")

    prog = load_progress()
    db = load_growth_db()
    stats, _ = check_daily_limits(db)

    # 1. Collect today's posts
    today_posts = []
    for item in prog.get("history", []):
        ts = item.get("timestamp", "")
        if ts.startswith(today_date_str):
            today_posts.append(item)

    # 2. Get live Instagram stats
    follower_count = "N/A"
    following_count = "N/A"
    media_count = "N/A"
    try:
        cl = init_client()
        uinfo = cl.user_info(cl.user_id)
        follower_count = uinfo.follower_count
        following_count = uinfo.following_count
        media_count = uinfo.media_count
        sync_follow_backs_and_analyze(cl, db)
    except Exception as e:
        print(f"[-] Notice reading profile metrics: {e}")

    # 3. Analyze Tag Performance
    tag_perf = db.get("tag_performance", {})
    best_tag = "Learning (#techfounder)"
    best_rate = "Calibrating..."
    if tag_perf:
        rated = [(t, s["rate"]) for t, s in tag_perf.items() if s.get("engaged", 0) > 0]
        if rated:
            rated.sort(key=lambda x: x[1], reverse=True)
            best_tag = f"#{rated[0][0]}"
            best_rate = f"{rated[0][1]}% follow-back"

    lines = [
        "📊 EXTROVERTNERD.DEV — DAILY EXECUTIVE REPORT",
        f"📅 Date: {today_formatted}",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"🚀 CONTENT PUBLISHED TODAY ({len(today_posts)} POSTS):",
    ]

    if today_posts:
        for idx, p in enumerate(today_posts, 1):
            s_name = p.get("session", "daily").capitalize()
            p_type = "Playbook" if p.get("type") == "curriculum" or p.get("day") else "Client Offer"
            lines.append(f"  {idx}. [{s_name} · {p_type}] {p.get('title')}")
    else:
        lines.append("  (No posts logged yet today)")

    lines.extend([
        "",
        "🌱 ORGANIC LEAD ENGAGEMENT TODAY:",
        f"  • 👤 Target Founders Followed: {stats.get('follows', 0)} / 25 max",
        f"  • ❤️ Founder Posts Liked: {stats.get('likes', 0)} / 40 max",
        f"  • 👁️ Active Stories Viewed: {stats.get('stories', 0)} / 80 max",
        f"  • 📋 Total Leads In Database: {len(db.get('interacted_users', {}))}",
        "",
        "🧠 AI SELF-TUNING ENGINE:",
        f"  • Top Converting Niche: {best_tag} ({best_rate})",
        "  • Optimization Strategy: Auto-shifting 75% outreach to highest-converting audiences",
        "",
        "📈 LIVE INSTAGRAM METRICS (@extrovertnerd.dev):",
        f"  • Followers: {follower_count}",
        f"  • Following: {following_count}",
        f"  • Total Feed Posts: {media_count}",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "💼 ACTION ITEMS FOR TONIGHT:",
        "  👉 Check Instagram DMs for 'AUDIT', 'TOOL', or 'BUILD' leads",
        "  👉 Check email inbox: extrovertnerd.dev@gmail.com",
        "",
        "System is running 100% autonomously in the cloud 🚀"
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
    parser = argparse.ArgumentParser(description="Multi-Session Daily Manager for @extrovertnerd.dev")
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
