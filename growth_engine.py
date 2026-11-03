#!/usr/bin/env python3
"""
Autonomous Instagram Growth & Client Acquisition Engine for @extrovertnerd.dev.
Executes organic, high-converting engagement (Story viewing, Targeted likes,
Lead follows, Clean unfollows, and Warm Lead Outreach).
Engineered with strict safety caps and randomized delays to keep your account 100% safe.
"""

import os
import sys
import json
import time
import random
import argparse
from datetime import datetime, timedelta
from instagrapi import Client

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
GROWTH_DB_FILE = os.path.join(DATA_DIR, "growth_state.json")
DEFAULT_SESSION_FILE = os.path.join(BASE_DIR, "ig_session.json")
os.makedirs(DATA_DIR, exist_ok=True)

# High-Intent Target Niches (Founders, Business Owners, Agencies, E-Commerce)
TARGET_HASHTAGS = [
    "buildinpublic",
    "indiehackers",
    "startuplife",
    "smallbusinessowner",
    "ecommercebusiness",
    "solopreneur",
    "shopifydropshipping",
    "saasstartup",
    "digitalagency",
    "techfounder",
    "growthhacking"
]

# Strict Daily Safety Caps (Tailored for new accounts to prevent flags)
MAX_DAILY_FOLLOWS = 25
MAX_DAILY_LIKES = 40
MAX_DAILY_STORY_VIEWS = 80
MIN_ACTION_DELAY_SEC = 35
MAX_ACTION_DELAY_SEC = 75

DM_TEMPLATE = (
    "Hey {name}! 👋 Great connecting with you. I build high-performance custom websites "
    "and internal automation tools for founders & businesses.\n\n"
    "If you ever want a free 5-minute video audit of your current website or want to "
    "automate any manual spreadsheets, feel free to give me a shout! 🚀"
)


def load_growth_db() -> dict:
    if os.path.exists(GROWTH_DB_FILE):
        try:
            with open(GROWTH_DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "interacted_users": {},
        "daily_stats": {},
        "last_run": None
    }


def save_growth_db(db: dict):
    with open(GROWTH_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


def get_today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def check_daily_limits(db: dict) -> tuple:
    today = get_today_str()
    stats = db["daily_stats"].get(today, {"follows": 0, "likes": 0, "stories": 0, "dms": 0})
    return stats, today


def init_client() -> Client:
    cl = Client()
    cl.set_user_agent(
        'Instagram 449.0.0.52.84 Android (34/14; 560dpi; 1440x3120; Google/google; Pixel 8 Pro; husky; husky; en_US; 652033084)'
    )

    # Session from env or file
    session_json = os.getenv("IG_SESSION_JSON")
    if session_json:
        try:
            cl.set_settings(json.loads(session_json))
        except Exception as e:
            print(f"[-] Error loading IG_SESSION_JSON env: {e}")

    if not cl.user_id and os.path.exists(DEFAULT_SESSION_FILE):
        cl.load_settings(DEFAULT_SESSION_FILE)

    if not cl.user_id:
        raise RuntimeError("Instagram session not found! Ensure ig_session.json exists.")

    return cl


def view_stories_for_users(cl: Client, user_ids: list, db: dict, max_count: int = 50) -> int:
    """Views stories of target leads. Extremely safe, triggers profile visits."""
    stats, today = check_daily_limits(db)
    viewed = 0

    print(f"\n👀 [growth_engine] Scanning active stories for {len(user_ids)} target leads...")

    for uid in user_ids:
        if stats["stories"] >= MAX_DAILY_STORY_VIEWS or viewed >= max_count:
            print(f"🛑 Reached daily story viewing limit ({MAX_DAILY_STORY_VIEWS}).")
            break

        try:
            stories = cl.user_stories(uid)
            if stories:
                story_pks = [s.pk for s in stories]
                cl.story_seen(story_pks)
                viewed += len(story_pks)
                stats["stories"] += len(story_pks)

                # Update DB
                uid_str = str(uid)
                if uid_str not in db["interacted_users"]:
                    db["interacted_users"][uid_str] = {}
                db["interacted_users"][uid_str]["stories_viewed_at"] = datetime.now().isoformat()
                db["daily_stats"][today] = stats
                save_growth_db(db)

                print(f"   👁️ Viewed {len(story_pks)} stories from lead (UID: {uid})")
                time.sleep(random.uniform(4, 10))
        except Exception as e:
            continue

    print(f"✅ Finished story blitz: {viewed} stories viewed.\n")
    return viewed


def safe_engage_leads(cl: Client, target_hashtag: str, max_follows: int = 10, max_likes: int = 15) -> dict:
    """Discovers high-potential leads from target hashtag and engages them safely."""
    db = load_growth_db()
    stats, today = check_daily_limits(db)

    print("\n" + "=" * 65)
    print(f"🚀 RUNNING SAFE ORGANIC GROWTH CYCLE (#{target_hashtag})")
    print(f"📊 Today's stats: {stats['follows']}/{MAX_DAILY_FOLLOWS} follows, {stats['likes']}/{MAX_DAILY_LIKES} likes")
    print("=" * 65)

    if stats["follows"] >= MAX_DAILY_FOLLOWS:
        print(f"🛑 Daily follow limit reached ({MAX_DAILY_FOLLOWS}). Halting to protect account safety.")
        return {"follows": 0, "likes": 0}

    print(f"[*] Fetching high-intent posts from #{target_hashtag}...")
    try:
        medias = cl.hashtag_medias_top(target_hashtag, amount=20)
    except Exception as e:
        print(f"[-] Error fetching hashtag medias: {e}")
        try:
            medias = cl.hashtag_medias_recent(target_hashtag, amount=20)
        except Exception:
            medias = []

    if not medias:
        print("[-] No media found for hashtag.")
        return {"follows": 0, "likes": 0}

    new_follows = 0
    new_likes = 0
    target_uids = []

    for m in medias:
        if new_follows >= max_follows or stats["follows"] >= MAX_DAILY_FOLLOWS:
            break

        user = m.user
        uid = str(user.pk)
        username = user.username

        # Avoid engaging with ourselves or already contacted users
        if uid == str(cl.user_id):
            continue
        if uid in db["interacted_users"] and db["interacted_users"][uid].get("followed"):
            continue

        target_uids.append(user.pk)

        # 1. Like their recent post
        if new_likes < max_likes and stats["likes"] < MAX_DAILY_LIKES:
            try:
                cl.media_like(m.id)
                new_likes += 1
                stats["likes"] += 1
                print(f"❤️ Liked post from @{username} (Media: {m.id})")
                time.sleep(random.uniform(5, 12))
            except Exception as e:
                print(f"[-] Like skipped for @{username}: {e}")

        # 2. Follow targeted user
        if new_follows < max_follows and stats["follows"] < MAX_DAILY_FOLLOWS:
            try:
                cl.user_follow(user.pk)
                new_follows += 1
                stats["follows"] += 1

                db["interacted_users"][uid] = {
                    "username": username,
                    "followed_at": datetime.now().isoformat(),
                    "followed": True,
                    "source_hashtag": target_hashtag
                }
                db["daily_stats"][today] = stats
                save_growth_db(db)

                print(f"👤 Followed target lead: @{username} (Total today: {stats['follows']}/{MAX_DAILY_FOLLOWS})")

                # Natural human jitter delay between follows
                delay = random.uniform(MIN_ACTION_DELAY_SEC, MAX_ACTION_DELAY_SEC)
                print(f"⏳ Sleeping {int(delay)}s to simulate natural browsing pattern...")
                time.sleep(delay)
            except Exception as e:
                print(f"[-] Follow skipped for @{username}: {e}")
                time.sleep(15)

    # 3. View stories of targets for maximum profile visibility
    if target_uids:
        view_stories_for_users(cl, target_uids, db, max_count=30)

    db["last_run"] = datetime.now().isoformat()
    db["daily_stats"][today] = stats
    save_growth_db(db)

    print("\n" + "=" * 65)
    print(f"🎉 GROWTH CYCLE COMPLETE:")
    print(f"   + Followed: {new_follows} targeted leads")
    print(f"   + Liked: {new_likes} founder posts")
    print("=" * 65 + "\n")

    return {"follows": new_follows, "likes": new_likes}


def clean_unfollow_non_reciprocal(cl: Client, older_than_days: int = 7, max_unfollows: int = 15) -> int:
    """Safely unfollows users who have not followed back after X days."""
    db = load_growth_db()
    print(f"\n🧹 [growth_engine] Checking for leads followed > {older_than_days} days ago...")

    try:
        my_followers = set(cl.user_followers(cl.user_id).keys())
    except Exception as e:
        print(f"[-] Error fetching followers: {e}")
        return 0

    cutoff = datetime.now() - timedelta(days=older_than_days)
    unfollowed = 0

    for uid, data in list(db["interacted_users"].items()):
        if unfollowed >= max_unfollows:
            break

        if not data.get("followed"):
            continue

        followed_at_str = data.get("followed_at")
        if not followed_at_str:
            continue

        followed_at = datetime.fromisoformat(followed_at_str)
        if followed_at < cutoff and int(uid) not in my_followers:
            try:
                cl.user_unfollow(int(uid))
                data["unfollowed_at"] = datetime.now().isoformat()
                data["followed"] = False
                unfollowed += 1
                print(f"✂️ Unfollowed inactive lead: @{data.get('username', uid)}")
                time.sleep(random.uniform(25, 50))
            except Exception as e:
                print(f"[-] Unfollow error for {uid}: {e}")

    save_growth_db(db)
    print(f"✅ Clean unfollow complete: {unfollowed} accounts updated.\n")
    return unfollowed


def send_warm_outreach(cl: Client, username: str, custom_text: str = None) -> bool:
    """Sends a professional, value-packed inquiry or audit offer to a qualified lead."""
    try:
        user_info = cl.user_info_by_username(username)
        uid = user_info.pk
        first_name = (user_info.full_name or username).split()[0].capitalize()
        message = custom_text or DM_TEMPLATE.format(name=first_name)

        cl.direct_send(message, user_ids=[uid])
        print(f"✉️ Successfully sent warm outreach to @{username}!")

        db = load_growth_db()
        today = get_today_str()
        stats, _ = check_daily_limits(db)
        stats["dms"] += 1
        db["daily_stats"][today] = stats
        save_growth_db(db)
        return True
    except Exception as e:
        print(f"[-] Direct outreach error for @{username}: {e}")
        return False


def print_account_summary(cl: Client):
    try:
        uinfo = cl.user_info(cl.user_id)
        db = load_growth_db()
        stats, today = check_daily_limits(db)

        print("\n" + "=" * 65)
        print(f"📊 INSTAGRAM GROWTH DASHBOARD: @{uinfo.username}")
        print("=" * 65)
        print(f"  Followers     : {uinfo.follower_count}")
        print(f"  Following     : {uinfo.following_count}")
        print(f"  Total Posts   : {uinfo.media_count}")
        print("-" * 65)
        print(f"  Today's Follows     : {stats['follows']} / {MAX_DAILY_FOLLOWS} max")
        print(f"  Today's Likes       : {stats['likes']} / {MAX_DAILY_LIKES} max")
        print(f"  Today's Story Views : {stats['stories']} / {MAX_DAILY_STORY_VIEWS} max")
        print(f"  Total Leads Tracked : {len(db['interacted_users'])}")
        print("=" * 65 + "\n")
    except Exception as e:
        print(f"[-] Error fetching profile stats: {e}")


def main():
    parser = argparse.ArgumentParser(description="Instagram Growth & Lead Gen Engine")
    parser.add_argument("--auto", action="store_true", help="Run the full safe organic growth cycle")
    parser.add_argument("--hashtag", type=str, default=None, help="Specific hashtag to target")
    parser.add_argument("--stories", action="store_true", help="View stories of target leads")
    parser.add_argument("--unfollow", action="store_true", help="Clean unfollow non-reciprocal leads older than 7 days")
    parser.add_argument("--dm", type=str, default=None, help="Send warm outreach DM to target username")
    parser.add_argument("--stats", action="store_true", help="Show live follower metrics and daily stats")

    args = parser.parse_args()

    cl = init_client()

    if args.stats:
        print_account_summary(cl)
        return

    if args.dm:
        send_warm_outreach(cl, args.dm)
        return

    if args.unfollow:
        clean_unfollow_non_reciprocal(cl)
        return

    # Pick a random high-converting niche hashtag
    target_tag = args.hashtag or random.choice(TARGET_HASHTAGS)

    if args.stories:
        medias = cl.hashtag_medias_top(target_tag, amount=20)
        uids = [m.user.pk for m in medias]
        db = load_growth_db()
        view_stories_for_users(cl, uids, db, max_count=40)
        return

    # Default: Run safe organic growth cycle
    safe_engage_leads(cl, target_tag, max_follows=12, max_likes=15)
    print_account_summary(cl)


if __name__ == "__main__":
    main()
