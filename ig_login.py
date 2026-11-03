#!/usr/bin/env python3
"""
One-time Instagram Authenticator for @extrovertnerd.dev.
Supports password authentication, email/SMS verification code challenges, and session export.
Once generated, the session is saved as ig_session.json and can be added as a GitHub Actions secret.
"""

import os
import sys
import json
from instagrapi import Client

def main():
    username = sys.argv[1] if len(sys.argv) > 1 else input("Enter Instagram username: ").strip()
    password = sys.argv[2] if len(sys.argv) > 2 else input("Enter Instagram password: ").strip()

    cl = Client()
    cl.set_user_agent(
        'Instagram 449.0.0.52.84 Android (34/14; 560dpi; 1440x3120; Google/google; Pixel 8 Pro; husky; husky; en_US; 652033084)'
    )

    cl.username = username
    cl.password = password

    print(f"\n[*] Authenticating as @{username}...")

    def challenge_code_handler(username, choice):
        print(f"\n⚠️ Instagram requested a verification challenge via {choice}.")
        print("Check your email (extrovertnerd.dev@gmail.com) or SMS for the 6-digit code.")
        code = input("👉 Enter the 6-digit code here: ").strip()
        return code

    cl.challenge_code_handler = challenge_code_handler

    try:
        # Attempt modern Bloks CAA login
        res = cl.bloks_caa_login()
        if not res.get("logged_in"):
            # Fallback to standard login
            cl.login(username, password)
    except Exception as e:
        print(f"[-] Login flow error: {e}")

    try:
        info = cl.account_info()
        print(f"\n🎉 Successfully authenticated as @{info.username} (ID: {info.pk})!")

        # Save session to promo and POSTER_100DAYS
        session_paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "ig_session.json"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "POSTER_100DAYS", "ig_session.json"),
        ]

        for sp in session_paths:
            os.makedirs(os.path.dirname(sp), exist_ok=True)
            cl.dump_settings(sp)
            print(f"✅ Session saved to {sp}")

        # Also print JSON string for GitHub Actions Secret
        with open(session_paths[0], "r") as f:
            sess_json = f.read()

        print("\n" + "=" * 65)
        print("📋 COPY THIS ENTIRE STRING INTO GITHUB SECRETS (IG_SESSION_JSON):")
        print("=" * 65)
        print(sess_json)
        print("=" * 65 + "\n")

    except Exception as e:
        print(f"[-] Could not verify account: {e}")

if __name__ == "__main__":
    main()
