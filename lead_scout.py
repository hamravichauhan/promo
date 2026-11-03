#!/usr/bin/env python3
"""
AI Lead Scout Engine for ExtrovertNerd Network:
Curates high-intent client prospects (Founders, CTOs, Agency Directors, E-com Brands)
categorized by session and niche. Dispatches a 1-tap engagement sheet to Telegram
with personalized conversation starters for 100% safe, ban-free organic growth.
"""

import os
import json
import random
from datetime import datetime, timezone, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
SCOUT_HISTORY_FILE = os.path.join(DATA_DIR, "scout_history.json")
os.makedirs(DATA_DIR, exist_ok=True)

from poster_dispatcher import send_telegram_text

IST = timezone(timedelta(hours=5, minutes=30))

# Curated high-intent target prospects organized by target persona
TARGET_PROSPECTS_DB = {
    "tech_founders": [
        {"username": "levelsio", "name": "Pieter Levels", "niche": "Indie SaaS & Nomad List", "angle": "Discuss lean tech stacks, server cost optimization, or Next.js edge caching."},
        {"username": "dannypostmaa", "name": "Danny Postma", "niche": "AI SaaS & HeadshotPro", "angle": "Compliment UX flow and offer sub-second load audit on new landing pages."},
        {"username": "tibo_maker", "name": "Tibo", "niche": "Tweet Hunter & Taplio Founder", "angle": "Ask about internal API rate limits and Next.js server actions."},
        {"username": "marckohlbrugge", "name": "Marc Kohlbrugge", "niche": "BetaList & Startup Founder", "angle": "Discuss rapid prototyping tools and high-converting landing page layouts."},
        {"username": "csallen", "name": "Courtland Allen", "niche": "Indie Hackers Founder", "angle": "Share insight on bootstrapping custom internal tools vs SaaS subscriptions."},
        {"username": "dagorenouf", "name": "Dago Renouf", "niche": "Logology & SaaS Branding", "angle": "Point out how Core Web Vitals directly amplify paid marketing ROI."},
        {"username": "swyx", "name": "Shawn Wang", "niche": "AI Engineer & Founder", "angle": "Discuss latency reduction on modern AI web wrappers and client interfaces."},
        {"username": "yongfook", "name": "Jon Yongfook", "niche": "Bannerbear & Micro-SaaS", "angle": "Compliment API uptime architecture and discuss automated background queues."},
        {"username": "johnrushx", "name": "John Rush", "niche": "MarsX & Ecosystem Builder", "angle": "Offer perspectives on building full micro-apps within 14-day sprint cycles."},
        {"username": "arvidkahl", "name": "Arvid Kahl", "niche": "Bootstrapped Founder & Author", "angle": "Discuss self-healing web systems and zero-overhead maintenance."},
        {"username": "tonydinh", "name": "Tony Dinh", "niche": "TypingMind & Indie Dev", "angle": "Share performance benchmark on React vs vanilla DOM for web apps."},
        {"username": "alexwestco", "name": "Alex West", "niche": "CyberLeads Founder", "angle": "Offer insights on automated scraping dashboards and client data portals."},
    ],
    "creative_agencies": [
        {"username": "pentagramdesign", "name": "Pentagram", "niche": "Global Brand & Digital Agency", "angle": "Offer white-label engineering for demanding, high-performance client sites."},
        {"username": "fantasyinteractive", "name": "Fantasy", "niche": "Product Innovation Agency", "angle": "Propose sub-second frontend development for interactive 3D/canvas web apps."},
        {"username": "metalab", "name": "MetaLab", "niche": "Product Design & Venture Studio", "angle": "Discuss turnkey full-stack engineering partnerships for seed-stage portfolio cos."},
        {"username": "hugeinc", "name": "Huge", "niche": "Experience Design Agency", "angle": "Highlight sub-second Core Web Vitals engineering to prevent bounce rates."},
        {"username": "ustwo", "name": "ustwo", "niche": "Digital Product Studio", "angle": "Offer dedicated sprint capacity for custom internal portals and MVPs."},
        {"username": "basicagency", "name": "BASIC/DEPT", "niche": "E-Commerce & Digital Branding", "angle": "Propose headless Next.js Shopify engineering to boost checkout speed by 40%."},
        {"username": "instrument", "name": "Instrument", "niche": "Digital Agency & Web Studio", "angle": "Offer reliable React/TypeScript sprint teams for agency overflow projects."},
        {"username": "focuslab", "name": "Focus Lab", "niche": "B2B Tech Brand & Web Studio", "angle": "Discuss seamless dev implementation for high-converting B2B SaaS sites."},
    ],
    "saas_startups": [
        {"username": "supabase", "name": "Supabase Community", "niche": "Open Source Firebase Alternative", "angle": "Showcase Postgres real-time dashboard implementations."},
        {"username": "resend", "name": "Resend", "niche": "Developer-First Email Platform", "angle": "Share how fast transactional email webhooks integrate into custom portals."},
        {"username": "linear_app", "name": "Linear", "niche": "High-Performance Issue Tracking", "angle": "Highlight the business impact of sub-100ms UI responsiveness in modern web tools."},
        {"username": "raycastapp", "name": "Raycast", "niche": "Mac Productivity Ecosystem", "angle": "Propose custom extension or web companion dashboard development."},
        {"username": "cal.com", "name": "Cal.com", "niche": "Open Source Scheduling", "angle": "Discuss white-label booking portals integrated into enterprise client workflows."},
        {"username": "posthog", "name": "PostHog", "niche": "Product Analytics & Session Replay", "angle": "Discuss tracking Core Web Vitals regressions via automated dashboards."},
    ],
    "ecommerce_brands": [
        {"username": "gymshark", "name": "Gymshark Tech", "niche": "High-Volume Direct-to-Consumer", "angle": "Highlight how 100ms latency reduction increases mobile checkout conversions by 1.1%."},
        {"username": "allbirds", "name": "Allbirds", "niche": "Sustainable DTC Apparel", "angle": "Offer a complimentary mobile speed audit comparing desktop vs 4G mobile LCP."},
        {"username": "kith", "name": "Kith", "niche": "High-Demand Drop E-Commerce", "angle": "Discuss edge caching architectures that resist high-traffic flash sale crashes."},
        {"username": "glossier", "name": "Glossier", "niche": "Beauty & Direct Consumer", "angle": "Share how headless Shopify frontends eliminate checkout bottlenecks."},
    ]
}


def load_scout_history() -> set:
    if os.path.exists(SCOUT_HISTORY_FILE):
        try:
            with open(SCOUT_HISTORY_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            pass
    return set()


def save_scout_history(history: set):
    with open(SCOUT_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(list(history), f, indent=2)


def get_session_prospects(session: str, count: int = 4) -> list:
    """Selects fresh, unengaged prospects tailored to the session audience."""
    session = (session or "morning").lower()
    history = load_scout_history()

    if session == "morning":
        # India / APAC Tech Founders & Indie Hackers
        category = "tech_founders"
    elif session == "midday":
        # UK / EU Creative Agencies & Studios
        category = "creative_agencies"
    elif session == "evening":
        # US East Coast Early-Stage SaaS
        category = "saas_startups"
    else:
        # US Prime Time B2B & E-commerce Brands
        category = random.choice(["tech_founders", "ecommerce_brands"])

    pool = TARGET_PROSPECTS_DB.get(category, TARGET_PROSPECTS_DB["tech_founders"])
    
    # Filter out recently engaged prospects if possible
    uncontacted = [p for p in pool if p["username"] not in history]
    if len(uncontacted) < count:
        # Reset memory if entire pool has been scouted
        history.clear()
        uncontacted = pool

    selected = random.sample(uncontacted, min(count, len(uncontacted)))

    for p in selected:
        history.add(p["username"])
    save_scout_history(history)

    return selected, category


def format_lead_scout_sheet(session: str, prospects: list, category_name: str) -> str:
    """Formats the lead sheet for 1-tap Telegram engagement."""
    session_title = session.capitalize()
    now_ist = datetime.now(IST).strftime("%H:%M IST")

    lines = [
        f"🎯 AI LEAD SCOUT — {session_title.upper()} TARGETS ({now_ist})",
        f"📂 Focus: {category_name.replace('_', ' ').title()}",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "💡 100% Safe Organic Engagement Strategy:",
        "Tap the links on your phone & leave a genuine 1-sentence thought. Authentic human interaction gets a ~30% follow-back rate with zero ban risk!",
        ""
    ]

    for idx, p in enumerate(prospects, 1):
        u = p["username"]
        lines.extend([
            f"👤 #{idx} · {p['name']} (@{u})",
            f"   🏢 Niche: {p['niche']}",
            f"   👉 Profile: https://instagram.com/{u}",
            f"   💬 Hook Angle: \"{p['angle']}\"",
            ""
        ])

    lines.extend([
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "⚡ Spend 2 mins on your phone connecting with these 4 leads."
    ])
    return "\n".join(lines)


def run_lead_scout(session: str = "morning") -> bool:
    """Runs the lead scout and dispatches the sheet to Telegram."""
    prospects, category = get_session_prospects(session, count=4)
    sheet_text = format_lead_scout_sheet(session, prospects, category)
    print("\n" + sheet_text + "\n")
    success = send_telegram_text(sheet_text)
    if success:
        print(f"✅ Lead Scout sheet for {session.upper()} dispatched to Telegram!")
    return success


if __name__ == "__main__":
    import sys
    sess = sys.argv[1] if len(sys.argv) > 1 else "morning"
    run_lead_scout(sess)
