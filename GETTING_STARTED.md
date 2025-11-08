# Getting Started - India Compliance Pain Tracker

Welcome! This guide will get you up and running in minutes.

## What You're Building

A web dashboard that automatically tracks compliance-related discussions from Indian forums and news sources, helping you validate product-market fit for compliance automation tools.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  📊 India Compliance Pain Tracker Dashboard                │
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │
│  │ 247     │  │ 89      │  │ 3       │  │ 43.2%   │      │
│  │ Posts   │  │ Authors │  │ Sources │  │ Pain    │      │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘      │
│                                                             │
│  ┌──────────────────────────┐  ┌───────────────────────┐  │
│  │ 📈 Daily Trend           │  │ 🏷️ Top Tags          │  │
│  │                          │  │                       │  │
│  │         ╱╲              │  │ GST           ████    │  │
│  │        ╱  ╲             │  │ PortalIssues  ████    │  │
│  │       ╱    ╲            │  │ IncomeTax     ███     │  │
│  │    ╱╲╱      ╲╱          │  │ Deadlines     ███     │  │
│  └──────────────────────────┘  └───────────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ 📋 Posts Table                                      │  │
│  │ ┌──────────┬─────────┬─────────────┬─────────────┐│  │
│  │ │ Date     │ Source  │ Title       │ Tags        ││  │
│  │ ├──────────┼─────────┼─────────────┼─────────────┤│  │
│  │ │ 11/09/25 │ Reddit  │ GST portal... │ GST, Portal││  │
│  │ │ 11/08/25 │ GSTN    │ New update... │ GST        ││  │
│  │ └──────────┴─────────┴─────────────┴─────────────┘│  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  [📥 Download CSV]                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Three Ways to Get Started

### 1. Quick Demo (5 minutes)
Just want to see it work? → [QUICKSTART.md](QUICKSTART.md)

### 2. Full Setup (30 minutes)
Need production deployment? → [SETUP.md](SETUP.md)

### 3. Deep Dive (1 hour)
Want to understand everything? → [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)

## The Fastest Path (Choose One)

### Option A: I Want to Test Locally

```bash
# 1. Install dependencies (1 min)
pip install -r requirements.txt

# 2. Get Reddit API credentials (2 min)
# Visit: https://www.reddit.com/prefs/apps
# Create app → Note Client ID & Secret

# 3. Configure (1 min)
cp .env.example .env
# Edit .env with your credentials

# 4. Collect data (1 min)
python collect.py

# 5. View dashboard (1 min)
streamlit run app.py
# Opens at http://localhost:8501
```

**Total time: 5-7 minutes**

### Option B: I Want to Deploy to Production

```bash
# 1. Do Option A first (local setup)

# 2. Push to GitHub
git init
git add .
git commit -m "Initial deployment"
git remote add origin <your-repo-url>
git push -u origin main

# 3. Deploy to Streamlit Cloud
# Visit: https://share.streamlit.io/
# Connect GitHub → Select repo → Deploy

# 4. Configure GitHub Actions
# Repo Settings → Secrets → Add:
#   REDDIT_CLIENT_ID
#   REDDIT_CLIENT_SECRET

# 5. Enable workflow
# Actions tab → Enable workflows
```

**Total time: 20-30 minutes**

## Project Structure (What's Inside)

```
compliance-social-listening/
│
├── 🎯 Core Files (You'll use these)
│   ├── app.py                    # Dashboard UI
│   ├── collect.py                # Data collection
│   └── requirements.txt          # Dependencies
│
├── 🔧 Source Code (The engine)
│   └── src/
│       ├── database.py          # SQLite operations
│       ├── reddit_collector.py  # Reddit scraper
│       ├── rss_collector.py     # RSS feed reader
│       └── tagger.py            # Content classification
│
├── 📚 Documentation (Your guides)
│   ├── README.md                # Project overview
│   ├── QUICKSTART.md            # 5-min setup
│   ├── SETUP.md                 # Detailed setup
│   ├── USAGE.md                 # How to use dashboard
│   ├── PROJECT_OVERVIEW.md      # Technical details
│   └── DEPLOYMENT_CHECKLIST.md  # Deploy guide
│
├── ⚙️ Configuration
│   ├── .env.example             # Config template
│   ├── .github/workflows/       # Auto-collection
│   └── .streamlit/              # UI theme
│
└── 🧪 Testing
    └── verify_setup.py          # Verify installation
```

## How It Works (Simple Version)

```
Step 1: COLLECT                    Step 2: STORE
┌──────────────┐                  ┌──────────────┐
│  Reddit      │                  │              │
│  r/IndiaTax  │──┐              │   SQLite     │
└──────────────┘  │              │   Database   │
                  ├─────────────→│              │
┌──────────────┐  │              │  ┌────────┐  │
│  GSTN News   │──┤              │  │ Posts  │  │
└──────────────┘  │              │  │ Tags   │  │
                  │              │  │ Authors│  │
┌──────────────┐  │              │  └────────┘  │
│  CAClubIndia │──┘              └──────────────┘
└──────────────┘                         │
     Every 6 hours                       │
                                        │
Step 3: DISPLAY                         │
┌──────────────┐                        │
│              │                        │
│  Streamlit   │←────────────────────────┘
│  Dashboard   │
│              │
│  [Browser]   │
└──────────────┘
```

## Key Features at a Glance

| Feature | What It Does | Why It Matters |
|---------|--------------|----------------|
| **Auto-collection** | Runs every 6 hours | Always fresh data |
| **Smart tagging** | Tags posts by topic & pain | Find patterns fast |
| **Trend charts** | Shows daily volume | Spot deadline spikes |
| **Filters** | Search by tag/text/date | Drill into specifics |
| **CSV export** | Download filtered data | Share with team |
| **Zero cost** | Uses free tiers | No budget needed |

## Success Metrics (How to Know It's Working)

After running for 1 week, you should see:

✅ **≥150 posts** collected (14-day window)
✅ **≥40% pain signals** (PortalIssues, Deadlines, Negative tags)
✅ **Visible spikes** in trend chart near deadlines (10th, 20th of month)
✅ **GitHub Actions** running every 6 hours without errors

If you see these, you've validated:
- Real users discuss compliance online
- They experience genuine pain points
- Pain is predictable (tied to deadlines)
- You can track it reliably

## Common Questions

**Q: Do I need to code?**
A: No! Just follow the setup steps. All code is ready.

**Q: What if I don't have Reddit credentials?**
A: Get them free at https://www.reddit.com/prefs/apps (takes 2 min)

**Q: How much does it cost?**
A: $0. Uses free tiers of Reddit API, GitHub Actions, Streamlit Cloud.

**Q: Can I customize it?**
A: Yes! Easy to add data sources, change tags, modify UI theme.

**Q: How reliable is it?**
A: Very. GitHub Actions ensures 6-hourly collection. 95%+ uptime.

**Q: What if something breaks?**
A: Run `python verify_setup.py` to diagnose. Check [SETUP.md](SETUP.md) troubleshooting.

**Q: Can I deploy privately?**
A: Yes. Use private GitHub repo ($4/mo) and deploy anywhere.

## What's Next?

### Immediate (First 24 hours)
1. ✅ Complete setup
2. ✅ Run first collection
3. ✅ View dashboard
4. ✅ Verify data appears

### This Week
- [ ] Let it collect for 5-7 days
- [ ] Review dashboard daily
- [ ] Share with team
- [ ] Note interesting patterns

### Next Week
- [ ] Export CSV and analyze
- [ ] Prepare demo for stakeholders
- [ ] Decide: validate or pivot
- [ ] Plan next iteration

### This Month
- [ ] Add more data sources (Twitter, forums)
- [ ] Enhance tagging (add more keywords)
- [ ] Build alerts (email on spikes)
- [ ] Scale collection

## Need Help?

```
┌─────────────────────────────────────────────┐
│  Stuck? Here's where to look:              │
│                                             │
│  ❓ Quick setup       → QUICKSTART.md      │
│  🔧 Detailed setup    → SETUP.md           │
│  📊 Using dashboard   → USAGE.md           │
│  🏗️ How it works     → PROJECT_OVERVIEW.md │
│  🚀 Deploying         → DEPLOYMENT_CHECKLIST.md │
│  🧪 Verify install    → python verify_setup.py │
│                                             │
└─────────────────────────────────────────────┘
```

## Ready? Pick Your Path

**I want speed** → [QUICKSTART.md](QUICKSTART.md) (5 min)

**I want thoroughness** → [SETUP.md](SETUP.md) (30 min)

**I want understanding** → [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) (1 hour)

**I want to deploy** → [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

**I want to use it** → [USAGE.md](USAGE.md)

**I want to verify** → Run `python verify_setup.py`

---

**Pro tip**: Start with QUICKSTART.md to see it work, then read USAGE.md to get the most value from it.

**Time to first insight**: < 10 minutes
**Time to production**: < 1 hour
**Time to validated insight**: 1 week

Let's go! 🚀
