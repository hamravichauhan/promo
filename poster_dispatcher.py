"""
Dispatcher module for 100-Day Web Playbook Posters.
Handles seamless dispatch to Telegram bot and direct publishing to Instagram.
Supports both local runs (.env / session file) and GitHub Actions (secrets & env vars).
"""

import os
import json
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Load local .env if present
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Fallback paths for local development
if not os.getenv("TELEGRAM_BOT_TOKEN"):
    for alt_env in [
        os.path.join(os.path.dirname(BASE_DIR), "POSTER_100DAYS", ".env"),
        "/Users/ravichauhan/Desktop/MY RROJECT /instagrapi/.env",
    ]:
        if os.path.exists(alt_env):
            load_dotenv(alt_env)
            break

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "9009008011:AAFn9g5l_wCOAsilKmLwBb7PKH9O2iVQ8ME").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "1432790039").strip()
DEFAULT_SESSION_FILE = os.getenv(
    "IG_SESSION_FILE",
    os.path.join(BASE_DIR, "ig_session.json")
)


def send_to_telegram(photo_path: str, caption_text: str = "") -> bool:
    """Sends the rendered high-res poster and caption to the Telegram bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN).strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID).strip()

    if not token or not chat_id:
        print("[-] Telegram credentials missing. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.")
        return False

    if not os.path.exists(photo_path):
        print(f"[-] Poster photo not found: {photo_path}")
        return False

    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    print(f"[*] Dispatching Day poster to Telegram (chat: {chat_id})...")

    # Telegram caption limit is 1024 chars for sendPhoto
    short_caption = caption_text[:1000] if len(caption_text) > 1000 else caption_text

    try:
        with open(photo_path, "rb") as photo:
            res = requests.post(
                url,
                data={"chat_id": chat_id, "caption": short_caption},
                files={"photo": photo},
                timeout=25
            )

        data = res.json()
        if res.status_code == 200 and data.get("ok"):
            print("✅ Successfully delivered poster to Telegram!")
            # If caption was truncated, send full text as follow-up
            if len(caption_text) > 1000:
                msg_url = f"https://api.telegram.org/bot{token}/sendMessage"
                requests.post(msg_url, json={"chat_id": chat_id, "text": caption_text}, timeout=15)
            return True
        else:
            err_desc = data.get("description", res.text)
            print(f"[-] Telegram dispatch error: {err_desc}")
            if "chat not found" in err_desc.lower():
                print("💡 NOTE: Please open @extrovertNerd_promo_bot in Telegram and tap /start once to initialize your chat.")
            return False
    except Exception as e:
        print(f"[-] Telegram send exception: {e}")
        return False


def upload_to_instagram(photo_path: str, caption_text: str, session_file: str = None) -> bool:
    """
    Uploads the poster directly to Instagram feed.
    Checks environment secret IG_SESSION_JSON, local session file, or credentials.
    """
    if not os.path.exists(photo_path):
        print(f"[-] Photo not found: {photo_path}")
        return False

    try:
        from instagrapi import Client
        cl = Client()
        cl.set_user_agent('Instagram 449.0.0.52.84 Android (34/14; 560dpi; 1440x3120; Google/google; Pixel 8 Pro; husky; husky; en_US; 652033084)')

        # Strategy 1: IG_SESSION_JSON environment secret (ideal for GitHub Actions)
        session_json_env = os.getenv("IG_SESSION_JSON", "").strip()
        if session_json_env:
            try:
                settings = json.loads(session_json_env)
                cl.set_settings(settings)
                print("[*] Loaded Instagram session from IG_SESSION_JSON environment secret.")
            except Exception as e:
                print(f"[-] Failed parsing IG_SESSION_JSON: {e}")

        # Strategy 2: Session file on disk
        if not cl.user_id:
            sess_path = session_file or DEFAULT_SESSION_FILE
            if not os.path.exists(sess_path) and os.path.exists("/Users/ravichauhan/Desktop/MY RROJECT /instagrapi/ig_session.json"):
                sess_path = "/Users/ravichauhan/Desktop/MY RROJECT /instagrapi/ig_session.json"

            if os.path.exists(sess_path):
                try:
                    cl.load_settings(sess_path)
                    print(f"[*] Loaded Instagram session from {sess_path}")
                except Exception as e:
                    print(f"[-] Failed loading session from {sess_path}: {e}")

        # Verify session
        logged_in = False
        try:
            if cl.user_id:
                info = cl.account_info()
                logged_in = True
                print(f"[*] Verified Instagram session for @{info.username} (ID: {info.pk})")
        except Exception as e:
            print(f"[-] Session verification notice: {e}")

        # Strategy 3: Login with IG_USERNAME and IG_PASSWORD if not yet logged in
        if not logged_in:
            ig_user = os.getenv("IG_USERNAME", "extrovertnerd.dev").strip()
            ig_pass = os.getenv("IG_PASSWORD", "@Bbapromax9823").strip()
            if ig_user and ig_pass:
                print(f"[*] Attempting login for @{ig_user}...")
                cl.username = ig_user
                cl.password = ig_pass
                try:
                    outcome = cl.bloks_caa_login()
                    if outcome.get("logged_in"):
                        logged_in = True
                        print(f"✅ Logged in successfully as @{ig_user}")
                        cl.dump_settings(session_file or DEFAULT_SESSION_FILE)
                except Exception as e:
                    print(f"[-] Login exception: {e}")

        if not logged_in:
            print("[-] Instagram authentication pending: Session or valid credentials required.")
            return False

        print(f"[*] Uploading poster to Instagram...")
        media = cl.photo_upload(path=photo_path, caption=caption_text)
        print(f"🎉 Successfully published to Instagram! Media ID: {media.pk}")
        return True
    except Exception as e:
        print(f"[-] Instagram upload exception: {e}")
        return False
