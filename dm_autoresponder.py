#!/usr/bin/env python3
"""
Intelligent Inbound Instagram DM Auto-Responder & Lead Qualifier for @extrovertnerd.dev.
1. Automatically replies to inbound messages ("hi", "hello", "BUILD", "AUDIT", "TOOL", etc.).
2. Qualifies the lead with tailored agency offerings (Websites, MVPs, Internal Dashboards, Audits).
3. Instantly forwards a high-priority alert to your Telegram bot so you never miss an inquiry!
"""

import os
import sys
import json
import time
from datetime import datetime
from instagrapi import Client

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DM_STATE_FILE = os.path.join(DATA_DIR, "dm_replied_state.json")
DEFAULT_SESSION_FILE = os.path.join(BASE_DIR, "ig_session.json")
os.makedirs(DATA_DIR, exist_ok=True)

from poster_dispatcher import send_telegram_text


def load_dm_state() -> dict:
    if os.path.exists(DM_STATE_FILE):
        try:
            with open(DM_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"replied_messages": {}, "total_replies": 0}


def save_dm_state(state: dict):
    with open(DM_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def get_tailored_reply(message_text: str, sender_name: str = "there") -> tuple:
    """Returns (reply_text, lead_intent)."""
    text = (message_text or "").strip().lower()

    # Intent 1: Free Website / Speed Audit
    if "audit" in text or "review" in text or "speed" in text:
        reply = (
            f"Hey {sender_name}! 👋 Thanks for reaching out.\n\n"
            "Drop your website URL here and I will record a personalized 15-minute video "
            "breakdown of your load speed bottlenecks, mobile UX flaws, and missed conversion opportunities! ⚡"
        )
        return reply, "WEBSITE AUDIT"

    # Intent 2: Custom Tools / Dashboards / Automations
    if "tool" in text or "automate" in text or "automation" in text or "dashboard" in text or "saas" in text:
        reply = (
            f"Hey {sender_name}! 🛠️ Great to connect.\n\n"
            "We engineer custom internal dashboards and automated software tools to eliminate manual spreadsheets "
            "and save teams 20+ hours every week.\n\n"
            "What repetitive tasks or SaaS subscriptions are giving you the most headache right now?"
        )
        return reply, "CUSTOM TOOL / AUTOMATION"

    # Intent 3: New Website / MVP / Build
    if "build" in text or "website" in text or "mvp" in text or "app" in text or "redesign" in text:
        reply = (
            f"Hey {sender_name}! 🚀 Excited to learn about your build.\n\n"
            "We build high-performance custom websites and MVP web apps (Next.js, sub-1s speed, zero plugin bloat) "
            "with a guaranteed 14-day turnaround.\n\n"
            "Are you looking to launch a brand new site, an MVP, or redesign an existing one? Drop your project vision!"
        )
        return reply, "NEW BUILD / WEBSITE"

    # Intent 4: General Greeting / Default ("Hi", "Hello", "Hey", "Dm", etc.)
    reply = (
        f"Hey {sender_name}! 👋 Thanks for reaching out to ExtrovertNerd.\n\n"
        "We engineer high-performance custom websites (sub-1s speed) and automated internal software tools for founders & businesses.\n\n"
        "How can we help your business?\n"
        "1️⃣ High-converting custom website or redesign\n"
        "2️⃣ Custom internal tool / dashboard / automation\n"
        "3️⃣ Free 15-minute website speed & conversion audit\n\n"
        "Drop a note on what you're working on and let's get you a custom scope within 24 hours! 🚀"
    )
    return reply, "GENERAL INQUIRY"


def check_and_reply_inbox(cl: Client = None) -> int:
    """Checks direct inbox and responds to new inbound messages."""
    if not cl:
        from growth_engine import init_client
        cl = init_client()

    state = load_dm_state()
    replied_ids = state["replied_messages"]
    replies_sent = 0

    print("\n📬 [dm_autoresponder] Checking Instagram Direct inbox...")
    try:
        threads = cl.direct_threads(amount=10)
    except Exception as e:
        print(f"[-] Error fetching inbox threads: {e}")
        return 0

    if not threads:
        print("[-] No inbox threads found.")
        return 0

    for thread in threads:
        if not thread.messages:
            continue

        newest_msg = thread.messages[0]
        msg_id = str(newest_msg.id)
        sender_uid = str(newest_msg.user_id)

        # 1. Skip if WE sent the last message (never reply to ourselves)
        if sender_uid == str(cl.user_id):
            continue

        # 2. Skip if already replied to this exact message
        if msg_id in replied_ids:
            continue

        # 3. Identify user info
        sender_username = "lead"
        sender_display_name = "there"
        if thread.users:
            sender_user = thread.users[0]
            sender_username = sender_user.username
            sender_display_name = (sender_user.full_name or sender_user.username).split()[0].capitalize()

        raw_text = getattr(newest_msg, "text", "") or ""
        print(f"\n📩 NEW INBOUND DM from @{sender_username}: \"{raw_text}\"")

        # 4. Generate tailored response
        reply_text, intent = get_tailored_reply(raw_text, sender_display_name)

        # 5. Send automated reply to Instagram thread
        try:
            cl.direct_answer(thread.id, reply_text)
            print(f"✅ Auto-replied to @{sender_username} [{intent}]")

            # 6. Save state to prevent duplicate replies
            replied_ids[msg_id] = {
                "username": sender_username,
                "incoming_text": raw_text,
                "reply_sent": reply_text,
                "intent": intent,
                "timestamp": datetime.now().isoformat(),
            }
            state["total_replies"] += 1
            save_dm_state(state)
            replies_sent += 1

            # 7. Forward instant alert to user's Telegram bot!
            alert_msg = (
                f"🚨 NEW INSTAGRAM CLIENT INQUIRY!\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 Lead: @{sender_username}\n"
                f"🏷️ Intent: {intent}\n"
                f"💬 Message: \"{raw_text}\"\n\n"
                f"🤖 Auto-Reply Sent:\n"
                f"\"{reply_text}\"\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👉 Open Instagram to chat with the client!"
            )
            send_telegram_text(alert_msg)
            print("📱 Telegram instant lead notification sent!")

            time.sleep(3)
        except Exception as e:
            print(f"[-] Error answering thread {thread.id}: {e}")

    print(f"\n✅ Inbox scan complete: {replies_sent} auto-replies delivered.\n")
    return replies_sent


def main():
    check_and_reply_inbox()


if __name__ == "__main__":
    main()
