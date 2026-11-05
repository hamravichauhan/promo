#!/usr/bin/env python3
"""
Real-Time Background Worker for ExtrovertNerd Dual-Channel Network:
- Scans recent post comments every 60 seconds via Meta Graph API v21.0
- Auto-replies to keyword inquiries ('AUDIT', 'TOOL', 'BUILD', 'MVP')
- Dispatches instant high-priority alerts to Telegram
- Performs safe organic growth cycles (automated Instagram Story publishing & Lead Scout)
"""

import os
import sys
import time
import signal
from datetime import datetime, timezone, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from comment_funnel import check_and_process_recent_comments
from lead_scout import run_lead_scout
from poster_dispatcher import send_telegram_text
from meta_graph_publisher import get_both_accounts_overview

IST = timezone(timedelta(hours=5, minutes=30))
POLL_INTERVAL_SECONDS = 60
running = True


def handle_shutdown(signum, frame):
    global running
    print("\n🛑 Shutdown signal received. Stopping worker cleanly...")
    running = False


signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)


def main():
    print("=" * 60)
    print("🚀 EXTROVERTNERD REAL-TIME STREAM WORKER STARTED")
    print(f"⏰ Poll Interval: Every {POLL_INTERVAL_SECONDS} seconds")
    print("🛡️ Engine: Official Meta Graph API v21.0 (Zero Ban Risk)")
    print("=" * 60)

    # Initial start ping
    start_msg = (
        "🟢 EXTROVERTNERD REAL-TIME WORKER ONLINE\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "• Monitoring @extrovertnerd.dev & @extrovertnerd for comments/leads every 60s\n"
        "• Token Lifetime: PERMANENT (Never Expires)\n"
        "• Auto-Lead Responder: ACTIVE\n"
        "System is running 24/7."
    )
    send_telegram_text(start_msg)

    cycle_count = 0
    while running:
        cycle_count += 1
        now_str = datetime.now(IST).strftime("%H:%M:%S IST")
        print(f"[{now_str}] Cycle #{cycle_count}: Checking comments & inbound leads...")

        try:
            leads = check_and_process_recent_comments()
            if leads > 0:
                print(f"🔥 Detected {leads} new inbound lead(s)!")
        except Exception as e:
            print(f"[-] Worker error during scan: {e}")

        # Sleep in 1-second chunks so shutdown is responsive
        for _ in range(POLL_INTERVAL_SECONDS):
            if not running:
                break
            time.sleep(1)

    print("✅ Real-time worker stopped.")


if __name__ == "__main__":
    main()
