#!/usr/bin/env python3
"""
Comment-to-DM Inbound Lead Funnel for ExtrovertNerd Dual-Channel Network:
Monitors comments across @extrovertnerd.dev and @extrovertnerd using official Meta Graph API v21.0.
Detects keyword triggers ('AUDIT', 'TOOL', 'BUILD', 'MVP', etc.), auto-replies publicly,
and instantly dispatches a high-priority Lead Alert to Telegram.
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_COMMENTS_FILE = os.path.join(DATA_DIR, "processed_comments.json")
INBOUND_LEADS_FILE = os.path.join(DATA_DIR, "inbound_leads.json")
os.makedirs(DATA_DIR, exist_ok=True)

from poster_dispatcher import send_telegram_text
from meta_graph_publisher import DEV_IG_ID, DEV_TOKEN, AGENCY_IG_ID, AGENCY_TOKEN, GRAPH_API_BASE

IST = timezone(timedelta(hours=5, minutes=30))

TRIGGER_KEYWORDS = [
    "AUDIT", "TOOL", "BUILD", "MVP", "PORTAL",
    "DASHBOARD", "AUTOMATE", "INFO", "YES", "INTERESTED", "DECK"
]


def load_processed_comments() -> set:
    if os.path.exists(PROCESSED_COMMENTS_FILE):
        try:
            with open(PROCESSED_COMMENTS_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            pass
    return set()


def save_processed_comments(processed: set):
    with open(PROCESSED_COMMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(processed), f, indent=2)


def record_inbound_lead(lead: dict):
    leads = []
    if os.path.exists(INBOUND_LEADS_FILE):
        try:
            with open(INBOUND_LEADS_FILE, "r", encoding="utf-8") as f:
                leads = json.load(f)
        except Exception:
            pass
    leads.append(lead)
    with open(INBOUND_LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2)


def get_account_recent_media(ig_id: str, token: str, limit: int = 5) -> list:
    """Fetches recent posts with permalinks and comment counts."""
    url = f"{GRAPH_API_BASE}/{ig_id}/media?fields=id,caption,permalink,comments_count,timestamp&limit={limit}&access_token={token}"
    try:
        req = urllib.request.urlopen(url, timeout=15)
        data = json.loads(req.read().decode("utf-8"))
        return data.get("data", [])
    except Exception as e:
        print(f"[-] Error fetching media for {ig_id}: {e}")
        return []


def get_media_comments(media_id: str, token: str) -> list:
    """Fetches comments for a specific media post."""
    url = f"{GRAPH_API_BASE}/{media_id}/comments?fields=id,text,username,timestamp,from&access_token={token}"
    try:
        req = urllib.request.urlopen(url, timeout=15)
        data = json.loads(req.read().decode("utf-8"))
        return data.get("data", [])
    except Exception as e:
        print(f"[-] Error fetching comments for {media_id}: {e}")
        return []


def reply_to_comment(comment_id: str, reply_text: str, token: str) -> bool:
    """Publishes a public reply to the comment."""
    url = f"{GRAPH_API_BASE}/{comment_id}/replies"
    data = urllib.parse.urlencode({
        "message": reply_text,
        "access_token": token
    }).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=15) as res:
            res_data = json.loads(res.read().decode("utf-8"))
            return "id" in res_data
    except Exception as e:
        print(f"[-] Notice replying to comment {comment_id}: {e}")
        return False


def dispatch_lead_alert_to_telegram(lead: dict) -> bool:
    """Sends immediate high-priority lead notification to Telegram."""
    lines = [
        "🚨 HIGH-INTENT INBOUND LEAD DETECTED!",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"👤 Lead: @{lead.get('username')}",
        f"💬 Comment: \"{lead.get('text')}\"",
        f"🎯 Trigger Keyword: #{lead.get('keyword')}",
        f"📱 Channel: @{lead.get('channel')}",
        f"🖼️ Post: {lead.get('permalink')}",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"👉 Action: Open Instagram and DM @{lead.get('username')} now!",
        f"🔗 Profile: https://instagram.com/{lead.get('username')}"
    ]
    msg = "\n".join(lines)
    print("\n" + msg + "\n")
    return send_telegram_text(msg)


def check_and_process_recent_comments() -> int:
    """Scans recent comments on both channels, replies to triggers, and alerts on Telegram."""
    processed = load_processed_comments()
    leads_detected = 0

    channels = [
        {"name": "extrovertnerd.dev", "ig_id": DEV_IG_ID, "token": DEV_TOKEN},
        {"name": "extrovertnerd", "ig_id": AGENCY_IG_ID, "token": AGENCY_TOKEN},
    ]

    for ch in channels:
        if not ch["ig_id"] or not ch["token"]:
            continue

        media_items = get_account_recent_media(ch["ig_id"], ch["token"], limit=5)
        for m in media_items:
            m_id = m.get("id")
            permalink = m.get("permalink", f"https://instagram.com/{ch['name']}")
            comments = get_media_comments(m_id, ch["token"])

            for c in comments:
                c_id = c.get("id")
                if not c_id or c_id in processed:
                    continue

                text = (c.get("text") or "").strip()
                username = c.get("username") or c.get("from", {}).get("username", "prospect")

                # Skip own comments
                if username.lower() in ["extrovertnerd.dev", "extrovertnerd"]:
                    processed.add(c_id)
                    continue

                # Check for trigger keywords
                matched_kw = None
                upper_text = text.upper()
                for kw in TRIGGER_KEYWORDS:
                    if kw in upper_text:
                        matched_kw = kw
                        break

                if matched_kw:
                    leads_detected += 1
                    lead_record = {
                        "comment_id": c_id,
                        "username": username,
                        "text": text,
                        "keyword": matched_kw,
                        "channel": ch["name"],
                        "permalink": permalink,
                        "timestamp": datetime.now(IST).isoformat(),
                    }

                    # 1. Attempt public reply
                    reply_text = f"Hey @{username}! Just sent you the details via DM. Check your message requests 🚀"
                    reply_to_comment(c_id, reply_text, ch["token"])

                    # 2. Dispatch alert to Telegram
                    dispatch_lead_alert_to_telegram(lead_record)

                    # 3. Record lead
                    record_inbound_lead(lead_record)

                processed.add(c_id)

    save_processed_comments(processed)
    print(f"[*] Comment Funnel Check Complete: {leads_detected} new leads detected.")
    return leads_detected


if __name__ == "__main__":
    check_and_process_recent_comments()
