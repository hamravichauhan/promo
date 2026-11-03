# 🚀 100-Day Web Playbook & Client Acquisition Poster Engine

Automated cloud-driven graphic design and lead generation pipeline. Runs **100% autonomously in the cloud via GitHub Actions** every day—even when your computer is shut down.

---

## ⚡ What It Does
1. **Generates Senior-Agency-Grade 4:5 Instagram Posters (1080x1350 Retina):**
   - Combines **real 1800px+ editorial photography** (servers, laptops, code, mobile UI, dashboards).
   - High-impact typography (`Montserrat-Black` + `Montserrat-Bold`).
   - Floating benchmark HUD overlays.
   - 3 actionable takeaway cards with high-contrast badge numbers.
   - **Executive Promotion Deck**:
     - Branded strictly as `@extrovertnerd.dev`
     - Direct CTA: *"DM for custom tools & websites"*
     - Contact Box: `💬 DM "BUILD" on Instagram: @extrovertnerd.dev`
     - Direct Email Box: `✉️ extrovertnerd.dev@gmail.com`
2. **Dispatches Directly to Telegram Bot:**
   - Sends the HD poster along with the complete post description and hashtags.
3. **Publishes Directly to Instagram Feed:**
   - Posts to `@extrovertnerd.dev` automatically.
4. **Auto-Advancement:**
   - Automatically tracks day progress (`data/progress.json`) across the 100-day curriculum.

---

## ⚙️ Daily Automation Schedule (GitHub Actions)
The workflow [`.github/workflows/daily_poster.yml`](.github/workflows/daily_poster.yml) runs automatically:
- **Every day at 10:00 AM IST** (`04:30 AM UTC`).
- Can also be triggered manually anytime via GitHub Actions **Run workflow** button.

---

## 🔑 GitHub Repository Secrets Setup
Go to **GitHub Repo → Settings → Secrets and variables → Actions** and add:

| Secret Name | Value / Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | `9009008011:AAFn9g5l_wCOAsilKmLwBb7PKH9O2iVQ8ME` |
| `TELEGRAM_CHAT_ID` | `1432790039` |
| `IG_USERNAME` | `extrovertnerd.dev` |
| `IG_PASSWORD` | Your Instagram password |
| `IG_SESSION_JSON` | *(Recommended)* Full JSON session export from instagrapi |

---

## 💻 Local CLI Usage
```bash
# Render specific day
python make_poster.py --day 1

# Render and advance today's poster + dispatch to Telegram & Instagram
python make_poster.py --today --send-telegram --upload-ig

# Batch render all 100 days
python make_poster.py --all

# View all 100 curriculum topics
python make_poster.py --list
```
