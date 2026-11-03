# 🚀 24/7 Multi-Session Client Acquisition & Growth Engine

Autonomous cloud-driven client acquisition engine for **[@extrovertnerd.dev](https://instagram.com/extrovertnerd.dev)**.

Runs **100% autonomously in the cloud via GitHub Actions** across **4 daily sessions** (Morning, Midday, Evening, and Night)—generating high-converting posters, delivering to Telegram, publishing to Instagram feed, naturally engaging targeted business owners, and sending a comprehensive **Daily Executive Summary Report** to your Telegram bot every night!

---

## 🕒 The 4 Daily Sessions (Indian Standard Time)

| Session | Time (IST) | What It Publishes | Organic Lead Engagement |
|---|---|---|---|
| **🌅 Morning** | **09:30 AM** | **Web Playbook Poster** (High-tech tip & Core Web Vitals) | 4-5 targeted founder follows + 6 likes + 15 story views |
| **☀️ Midday** | **01:30 PM** | **Client Offer Poster** (e.g. *"Why 85% of Sites Leak Leads"*) | Story viewing blitz (25 stories) + 4-5 targeted founder follows |
| **🌇 Evening** | **05:30 PM** | **Web Playbook Poster** (Tech architecture / CRO tip) | 4-5 targeted founder follows + 6 likes + 15 story views |
| **🌙 Night** | **09:30 PM** | **Client Offer Poster** (e.g. *"Stop Paying $500/Mo for SaaS"*) | Final micro engagement + **Sends Full Day Executive Report to Telegram!** |

---

## 📊 End-Of-Day Telegram Executive Report
Every night at **09:30 PM IST**, your Telegram bot ([@extrovertNerd_promo_bot](https://t.me/extrovertNerd_promo_bot)) automatically compiles and delivers:
1. **All 4 Posts Published Today** with titles and categories.
2. **Total Organic Actions**: Founders followed, posts liked, and active stories viewed.
3. **Live Profile Metrics**: Follower count, following count, total feed posts.
4. **Actionable Call-to-Action**: Reminds you to check DMs and email (`extrovertnerd.dev@gmail.com`) for inbound client inquiries!

---

## 💻 Manual CLI Usage

```bash
# 1. Run specific session manually
python daily_manager.py --session morning
python daily_manager.py --session midday
python daily_manager.py --session evening
python daily_manager.py --session night

# 2. Send End-of-Day Executive Summary Report to Telegram right now
python daily_manager.py --report

# 3. Check live account metrics and today's growth stats
python growth_engine.py --stats

# 4. Clean unfollow non-reciprocal accounts older than 7 days
python growth_engine.py --unfollow
```
