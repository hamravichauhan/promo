"""
Dispatcher module for 100-Day Web Playbook Posters.
Handles seamless dispatch to Telegram bot and direct publishing to Instagram.
Supports both local runs (.env / session file) and GitHub Actions (secrets & env vars).
Pure standard-library compatible with optional requests/dotenv acceleration.
"""

import os
import json
import urllib.request
import urllib.parse
import mimetypes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Load local .env
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(BASE_DIR, ".env"))
except ImportError:
    env_file = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip('"').strip("'")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()


def send_telegram_text(message: str) -> bool:
    """Sends a formatted text message (such as the End-of-Day Executive Report) to the Telegram bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN).strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID).strip()

    if not token or not chat_id:
        print("[-] Telegram credentials missing.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": message}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            data = json.loads(res.read().decode("utf-8"))
            return data.get("ok", False)
    except Exception as e:
        print(f"[-] Telegram text exception: {e}")
        return False


def send_to_telegram(photo_path_or_url: str, caption_text: str = "") -> bool:
    """Sends the rendered poster and caption to the Telegram bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN).strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID).strip()

    if not token or not chat_id:
        print("[-] Telegram credentials missing. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.")
        return False

    short_caption = caption_text[:1000] if len(caption_text) > 1000 else caption_text

    # If it's a URL or if requests is available
    if photo_path_or_url.startswith("http://") or photo_path_or_url.startswith("https://"):
        url = f"https://api.telegram.org/bot{token}/sendPhoto"
        payload = json.dumps({"chat_id": chat_id, "photo": photo_path_or_url, "caption": short_caption}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=25) as res:
                data = json.loads(res.read().decode("utf-8"))
                if data.get("ok"):
                    print("✅ Successfully delivered poster to Telegram via URL!")
                    return True
        except Exception as e:
            print(f"[-] Telegram URL send exception: {e}")

    # If it's a local file path, use multipart form data
    if os.path.exists(photo_path_or_url):
        boundary = "----TelegramFormBoundary" + os.urandom(16).hex()
        body = []

        # chat_id field
        body.append(f"--{boundary}".encode("utf-8"))
        body.append(f'Content-Disposition: form-data; name="chat_id"'.encode("utf-8"))
        body.append(b"")
        body.append(str(chat_id).encode("utf-8"))

        # caption field
        body.append(f"--{boundary}".encode("utf-8"))
        body.append(f'Content-Disposition: form-data; name="caption"'.encode("utf-8"))
        body.append(b"")
        body.append(short_caption.encode("utf-8"))

        # photo file field
        filename = os.path.basename(photo_path_or_url)
        mime_type = mimetypes.guess_type(photo_path_or_url)[0] or "application/octet-stream"
        body.append(f"--{boundary}".encode("utf-8"))
        body.append(f'Content-Disposition: form-data; name="photo"; filename="{filename}"'.encode("utf-8"))
        body.append(f"Content-Type: {mime_type}".encode("utf-8"))
        body.append(b"")
        with open(photo_path_or_url, "rb") as f:
            body.append(f.read())

        body.append(f"--{boundary}--".encode("utf-8"))
        body.append(b"")
        payload = b"\r\n".join(body)

        url = f"https://api.telegram.org/bot{token}/sendPhoto"
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "Content-Length": str(len(payload))
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                data = json.loads(res.read().decode("utf-8"))
                if data.get("ok"):
                    print("✅ Successfully delivered local poster to Telegram!")
                    return True
                else:
                    print(f"[-] Telegram sendPhoto error: {data}")
                    return False
        except Exception as e:
            print(f"[-] Telegram multipart send exception: {e}")
            return False

    print(f"[-] Photo source not found or failed: {photo_path_or_url}")
    return False


def upload_to_instagram(photo_path: str, caption_text: str, session_file: str = None) -> bool:
    """Legacy compatibility wrapper directing to meta_graph_publisher."""
    from meta_graph_publisher import publish_image_to_instagram
    raw_name = os.path.basename(photo_path)
    url = f"https://raw.githubusercontent.com/hamravichauhan/promo/main/output/{raw_name}"
    res = publish_image_to_instagram(url, caption_text, target="dev")
    return bool(res and res.get("success"))
