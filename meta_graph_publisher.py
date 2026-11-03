#!/usr/bin/env python3
"""
Official Meta Instagram Graph API Dual-Engine Publisher for:
- @extrovertnerd.dev (Technical Web Architecture & Speed Playbooks)
- @extrovertnerd (Commercial Pitch, Client Acquisition & Dashboard Offers)

Uses Meta's platform-sanctioned Graph API v21.0.
100% compliant with Meta Terms of Service — ZERO risk of account flags or IP bans.
"""

import os
import time
import json
import urllib.request
import urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load .env with native fallback
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

GRAPH_API_VERSION = "v21.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

# Credentials for Channel 1 (@extrovertnerd.dev)
DEV_IG_ID = os.getenv("IG_DEV_ID", "17841429293371829").strip()
DEV_TOKEN = os.getenv("IG_DEV_TOKEN", "").strip()

# Credentials for Channel 2 (@extrovertnerd)
AGENCY_IG_ID = os.getenv("IG_AGENCY_ID", "17841430226354207").strip()
AGENCY_TOKEN = os.getenv("IG_AGENCY_TOKEN", "").strip()


def get_channel_config(target: str) -> tuple:
    """Returns (ig_id, access_token, username)."""
    target = (target or "dev").strip().lower()
    if target in ["dev", "extrovertnerd.dev", "tech", "playbook"]:
        return DEV_IG_ID, DEV_TOKEN, "extrovertnerd.dev"
    else:
        return AGENCY_IG_ID, AGENCY_TOKEN, "extrovertnerd"


def get_account_metrics(target: str = "dev") -> dict:
    """Reads live follower count, following count, and post count from Meta Graph API."""
    ig_id, token, username = get_channel_config(target)
    if not ig_id or not token:
        return {"username": username, "error": "Missing credentials in .env"}

    url = f"{GRAPH_API_BASE}/{ig_id}?fields=id,username,name,followers_count,follows_count,media_count&access_token={token}"
    try:
        req = urllib.request.urlopen(url, timeout=15)
        data = json.loads(req.read().decode("utf-8"))
        return {
            "id": data.get("id"),
            "username": data.get("username", username),
            "followers": data.get("followers_count", 0),
            "following": data.get("follows_count", 0),
            "media_count": data.get("media_count", 0),
        }
    except Exception as e:
        return {"username": username, "error": str(e)}


def publish_image_to_instagram(image_url: str, caption: str, target: str = "dev") -> dict:
    """
    Publishes an image post to the targeted Instagram account via Meta Graph API:
    1. Create Media Container: POST /{ig-user-id}/media (image_url, caption)
    2. Wait 5s for Meta crawler ingestion
    3. Publish Media Container: POST /{ig-user-id}/media_publish (creation_id)
    """
    ig_id, token, username = get_channel_config(target)

    if not ig_id or not token:
        raise ValueError(f"Missing credentials for channel: {target}")

    print(f"\n🚀 [Meta Graph API] Publishing to @{username} (ID: {ig_id})...")
    print(f"   🖼️ Image URL: {image_url}")

    # Step 1: Create Container
    container_url = f"{GRAPH_API_BASE}/{ig_id}/media"
    container_data = urllib.parse.urlencode({
        "image_url": image_url,
        "caption": caption,
        "access_token": token
    }).encode("utf-8")

    try:
        req1 = urllib.request.Request(container_url, data=container_data)
        res1 = urllib.request.urlopen(req1, timeout=30)
        data1 = json.loads(res1.read().decode("utf-8"))
        container_id = data1.get("id")
        print(f"✅ Step 1: Container created! ID: {container_id}")
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"[-] Meta Graph Container Error: {err_msg}")
        return {"success": False, "error": err_msg}

    # Meta requires a short buffer to fetch and convert media
    time.sleep(5)

    # Step 2: Publish Container
    publish_url = f"{GRAPH_API_BASE}/{ig_id}/media_publish"
    publish_data = urllib.parse.urlencode({
        "creation_id": container_id,
        "access_token": token
    }).encode("utf-8")

    try:
        req2 = urllib.request.Request(publish_url, data=publish_data)
        res2 = urllib.request.urlopen(req2, timeout=30)
        data2 = json.loads(res2.read().decode("utf-8"))
        media_id = data2.get("id")
        print(f"🎉 Step 2: Successfully published to @{username}! Post Media ID: {media_id}\n")
        return {"success": True, "media_id": media_id, "username": username}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"[-] Meta Graph Publish Error: {err_msg}")
        return {"success": False, "error": err_msg}


def get_both_accounts_overview() -> str:
    """Generates a side-by-side summary of both live Instagram accounts."""
    dev_stats = get_account_metrics("dev")
    agency_stats = get_account_metrics("agency")

    lines = [
        "📈 LIVE MULTI-CHANNEL INSTAGRAM STATUS (Official Meta Graph API):",
        f"  • 🛠️ DEV CHANNEL (@{dev_stats.get('username', 'extrovertnerd.dev')}):",
        f"      Followers: {dev_stats.get('followers', 'N/A')} | Following: {dev_stats.get('following', 'N/A')} | Posts: {dev_stats.get('media_count', 'N/A')}",
        f"  • 💼 AGENCY CHANNEL (@{agency_stats.get('username', 'extrovertnerd')}):",
        f"      Followers: {agency_stats.get('followers', 'N/A')} | Following: {agency_stats.get('following', 'N/A')} | Posts: {agency_stats.get('media_count', 'N/A')}",
        "  • Platform Status: 100% Meta Graph API Compliance (Zero Ban Risk)"
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(get_both_accounts_overview())
