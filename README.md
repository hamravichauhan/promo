# 🚀 Autonomous Web Playbook & Client Acquisition Growth Engine

An end-to-end, cloud-automated Instagram growth and client acquisition system for **[@extrovertnerd.dev](https://instagram.com/extrovertnerd.dev)**.

Runs **100% autonomously in the cloud via GitHub Actions** every morning at 10:00 AM IST—generating high-converting posters, delivering to Telegram, posting to Instagram, and actively growing your audience with targeted business owners and founders.

---

## ⚡ What It Does

### 1. 🎨 Dual Poster Generation Engine (1080x1350 Retina)
* **100-Day Web Playbook Posters**: Real editorial photography, Core Web Vitals HUDs, 3 actionable takeaways, and bottom executive promotion card.
* **Client Acquisition & Offer Posters**: Dedicated pitch teardowns, SaaS replacement offers, free website audit hooks, ROI proof metrics, and direct DM calls-to-action (DM "AUDIT", "TOOL", "BUILD", "MVP").

### 2. 📱 Instant Multi-Channel Dispatch
* **Telegram Bot** ([@extrovertNerd_promo_bot](https://t.me/extrovertNerd_promo_bot)): Dispatches the HD poster and formatted post caption with the bio hook.
* **Instagram Feed** ([@extrovertnerd.dev](https://instagram.com/extrovertnerd.dev)): Directly publishes to your profile feed.

### 3. 🌱 Autonomous Organic Follower Growth (`growth_engine.py`)
* **Niche Lead Targeting**: Discovers founders, entrepreneurs, and ecommerce brand owners across high-intent hashtags (`#buildinpublic`, `#startuplife`, `#smallbusinessowner`, `#indiehackers`, `#saasstartup`).
* **Story Viewing Blitz**: Safely views 50-80 stories per day from targeted business owners to drive curiosity profile visits back to `@extrovertnerd.dev`.
* **Safe Organic Follows & Likes**: Automatically likes recent posts and follows 10-15 high-potential clients daily with randomized human delays (35-75s) to remain 100% within Instagram safety limits.
* **Clean Unfollow Maintenance**: Safely unfollows non-reciprocal accounts after 7 days to preserve a pristine follower-to-following ratio.
* **Warm Lead Outreach**: Pre-configured DM templates to send value-packed audit offers to interested founders.

---

## ⚙️ Cloud Automation Schedule (GitHub Actions)
The workflow [`.github/workflows/daily_poster.yml`](.github/workflows/daily_poster.yml) runs every day at **10:00 AM IST**:
1. Generates today's poster.
2. Sends HD image + caption to Telegram.
3. Publishes to Instagram feed.
4. Executes the safe organic growth cycle.
5. Advances queue and commits state back to git.

---

## 💻 CLI Usage

```bash
# 1. Check live account metrics and today's growth stats
python growth_engine.py --stats

# 2. Run safe organic growth cycle manually
python growth_engine.py --auto

# 3. Clean unfollow non-reciprocal accounts older than 7 days
python growth_engine.py --unfollow

# 4. Generate & dispatch today's playbook poster + run growth
python make_poster.py --today --send-telegram --upload-ig --grow

# 5. Generate & dispatch a high-converting Client Acquisition Offer
python make_poster.py --promo --send-telegram --upload-ig

# 6. List all 100 curriculum topics & client acquisition offers
python make_poster.py --list
```
