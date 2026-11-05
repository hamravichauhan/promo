#!/usr/bin/env python3
"""
Instagram Reels Automation Bridge for ExtrovertNerd Network:
Connects the /VIDEO GEN automated video engine with official Meta Graph API v21.0.
Generates vertical 9:16 videos with AI voiceover, kinetic subtitles, and SFX,
and streams them directly to Instagram Reels with zero ban risk.
"""

import os
import sys
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_GEN_DIR = os.path.join(os.path.dirname(BASE_DIR), "VIDEO GEN")

from poster_dispatcher import send_telegram_text


def generate_and_publish_reel(
    topic: int = 0,
    lang: str = "en",
    target: str = "dev",
    email: str = "extrovertnerd.dev@gmail.com",
    dm: str = "@extrovertnerd.dev"
) -> bool:
    """Executes the video generator and publishes the Reel to Instagram."""
    script_path = os.path.join(VIDEO_GEN_DIR, "make_web_tips_reel.py")
    if not os.path.exists(script_path):
        print(f"[-] Video generator script not found at: {script_path}")
        return False

    print("\n" + "=" * 60)
    print("🎬 LAUNCHING AUTOMATED REEL GENERATION & META GRAPH UPLOAD")
    print(f"🎯 Target Channel : @{target}")
    print(f"📌 Topic Index    : {topic}")
    print(f"🌐 Language       : {lang.upper()}")
    print("=" * 60 + "\n")

    cmd = [
        "/usr/bin/python3",
        script_path,
        "--topic", str(topic),
        "--lang", lang,
        "--email", email,
        "--dm", dm,
        "--upload-ig"
    ]

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        live_log = []
        for line in proc.stdout:
            sys.stdout.write(line)
            live_log.append(line)
        proc.wait()

        if proc.returncode == 0:
            print("✅ Reel generated and published successfully!")
            
            # Send Telegram confirmation
            tg_text = (
                "🎉 NEW INSTAGRAM REEL PUBLISHED LIVE!\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"• Target: @{dm}\n"
                f"• Engine: Official Meta Graph API v21.0 (Direct Binary Stream)\n"
                "• Audio: Broadcast Mastered -14 LUFS Voiceover\n"
                "• Visuals: 9:16 Kinetic Subtitles & Motion Photography\n"
                "Reel is now circulating on the Explore & Reels feed! 🚀"
            )
            send_telegram_text(tg_text)
            return True
        else:
            print(f"[-] Reel generation process exited with code {proc.returncode}")
            return False
    except Exception as e:
        print(f"[-] Reel automation exception: {e}")
        return False


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate and publish Reel via Meta Graph API")
    parser.add_argument("--topic", type=int, default=0, help="Topic index (0-3)")
    parser.add_argument("--lang", type=str, default="en", choices=["en", "hi"])
    parser.add_argument("--channel", type=str, default="dev", choices=["dev", "agency"])
    args = parser.parse_args()

    dm_handle = "@extrovertnerd.dev" if args.channel == "dev" else "@extrovertnerd"
    generate_and_publish_reel(topic=args.topic, lang=args.lang, target=args.channel, dm=dm_handle)
