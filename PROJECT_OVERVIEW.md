# India Compliance Pain Tracker - Project Overview

## What This Is

A lightweight, production-ready web application that tracks and visualizes compliance-related pain signals from Indian public forums and news sources. Built to validate product-market fit in the compliance automation space.

## Project Structure

```
compliance-social-listening/
│
├── app.py                          # Main Streamlit dashboard UI
├── collect.py                      # Data collection orchestrator
├── requirements.txt                # Python dependencies
│
├── src/                            # Core modules
│   ├── __init__.py
│   ├── database.py                # SQLite schema and queries
│   ├── reddit_collector.py        # Reddit data collector (PRAW)
│   ├── rss_collector.py           # RSS feed collector
│   └── tagger.py                  # Keyword-based content tagging
│
├── .github/workflows/
│   └── collect.yml                # GitHub Actions for auto-collection (every 6h)
│
├── .streamlit/
│   └── config.toml                # Streamlit UI configuration
│
├── .env.example                   # Template for environment variables
├── .gitignore                     # Git ignore rules
│
└── docs/
    ├── README.md                  # Main documentation
    ├── QUICKSTART.md              # 5-minute setup guide
    ├── SETUP.md                   # Detailed setup instructions
    ├── USAGE.md                   # Dashboard usage guide
    └── PROJECT_OVERVIEW.md        # This file
```

## Key Features

### Data Collection
- **Reddit**: r/IndiaTax, r/IndiaStartups
- **RSS**: GSTN News & Updates, CAClubIndia Tax News
- **Frequency**: Every 6 hours (automated via GitHub Actions)
- **Relevance filtering**: Keyword-based detection for compliance topics
- **Deduplication**: Prevents duplicate entries

### Content Tagging
Auto-tags posts into:

**Topics**:
- GST (GSTR, e-invoice, IRN, e-way bill)
- IncomeTax (ITR, refunds, returns)
- TDS/TCS (TRACES, returns)
- PF/ESI/PT (EPFO, ESIC, payroll taxes)
- MCA/ROC (company filings)
- Registration (PAN, TAN, DSC, etc.)

**Pain Signals**:
- PortalIssues (down, errors, login, OTP)
- Deadlines (due dates, penalties, late fees)
- Negative (errors, failures, frustration)

### Dashboard
- **KPIs**: Total posts, unique authors, pain signal %
- **Trend chart**: Daily mentions over time
- **Top tags**: Most common topics and pain points
- **Data table**: Searchable, filterable posts with links
- **CSV export**: Download filtered results
- **Filters**: Date range, source, tags, text search

## Technology Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| **UI** | Streamlit | Fast prototyping, no frontend code |
| **Data Collection** | PRAW + feedparser | Battle-tested Reddit/RSS libraries |
| **Storage** | SQLite | Single-file, zero-config, portable |
| **Scheduling** | GitHub Actions | Free, reliable, no server needed |
| **Tagging** | Regex + keywords | Transparent, fast, no ML overhead |
| **Hosting** | Streamlit Cloud | Free tier, auto-deploys from Git |

## Data Flow

```
┌─────────────────────────────────────────────────────────┐
│  Data Sources                                           │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐   │
│  │ Reddit   │  │ GSTN RSS │  │ CAClubIndia RSS    │   │
│  │ r/India  │  │          │  │                    │   │
│  │ Tax      │  │          │  │                    │   │
│  └────┬─────┘  └────┬─────┘  └─────────┬──────────┘   │
└───────┼─────────────┼──────────────────┼──────────────┘
        │             │                  │
        └─────────────┴──────────────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │  collect.py           │
          │  (Orchestrator)       │
          └───────────┬───────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌─────────────┐ ┌──────────┐ ┌──────────┐
│ Relevance   │ │ Content  │ │ Dedupe   │
│ Filter      │ │ Tagging  │ │ Check    │
└─────┬───────┘ └────┬─────┘ └────┬─────┘
      │              │            │
      └──────────────┴────────────┘
                     │
                     ▼
            ┌────────────────┐
            │  SQLite DB     │
            │  (Single File) │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │  app.py        │
            │  (Dashboard)   │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │  Streamlit UI  │
            │  (Browser)     │
            └────────────────┘
```

## Success Metrics (MVP Goals)

| Metric | Target | Purpose |
|--------|--------|---------|
| **Posts/14d** | ≥150 | Sufficient signal |
| **Pain Signal %** | ≥40% | Real problem validation |
| **Spikes** | Visible near deadlines | Predictable pain patterns |
| **Collection uptime** | ≥95% | Reliable automation |

## Deployment Options

### Option 1: Local Development
```bash
python collect.py  # Manual collection
streamlit run app.py  # Local dashboard
```

### Option 2: Streamlit Cloud (Recommended)
- Push to GitHub
- Connect to Streamlit Cloud
- Add Reddit credentials to secrets
- Auto-deploys on push
- GitHub Actions handles collection
- Free tier: unlimited for public repos

### Option 3: Self-Hosted
- Deploy to any Python-capable server
- Use cron for scheduling
- Serve with `streamlit run app.py --server.port 80`

## Configuration

### Environment Variables (.env)
```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=IndiaCompliancePainTracker/1.0
```

### Customization Points

**Add data sources** → Edit `collect.py`, create new collector
**Change tags** → Edit `src/tagger.py` keywords
**Adjust collection frequency** → Edit `.github/workflows/collect.yml` cron
**UI theme** → Edit `.streamlit/config.toml`
**Target subreddits** → Edit `src/reddit_collector.py` TARGET_SUBREDDITS
**RSS feeds** → Edit `src/rss_collector.py` RSS_FEEDS

## Development Workflow

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env
# Add your Reddit credentials to .env

# Develop
python collect.py              # Test collection
streamlit run app.py           # Test dashboard
python src/tagger.py           # Test tagging logic

# Deploy
git add .
git commit -m "Description"
git push origin main
# GitHub Actions auto-runs collection
# Streamlit Cloud auto-deploys dashboard
```

## Extending the Project

### Add Twitter/X Collection
1. Create `src/twitter_collector.py` (use tweepy)
2. Add Twitter credentials to `.env`
3. Import in `collect.py` and call in main()
4. Update dashboard source filter

### Add Sentiment Analysis
1. Add `transformers` or `textblob` to requirements.txt
2. Create `src/sentiment.py` with analyze() function
3. Store sentiment score in database (add column)
4. Show sentiment distribution in dashboard

### Add Alerts
1. Create `src/alerting.py`
2. Define alert rules (e.g., >50 posts/day with PortalIssues)
3. Integrate with email/Slack/Discord webhooks
4. Run in `collect.py` after collection

### Add User Authentication
1. Use `streamlit-authenticator` package
2. Add user management to dashboard
3. Store user preferences in database
4. Allow custom tag definitions per user

## Performance Characteristics

| Metric | Value |
|--------|-------|
| **Collection time** | 2-5 minutes |
| **Dashboard load** | < 2 seconds |
| **Database size** | ~5MB / 1000 posts |
| **Memory usage** | ~150MB |
| **Concurrent users** | ~10 (Streamlit free tier) |

## Security & Privacy

- **Read-only**: Only reads public posts, never writes or modifies
- **No PII**: Doesn't collect emails, IPs, or private info
- **Rate limiting**: Respects Reddit API rate limits
- **Attribution**: Links back to original posts
- **ToS compliant**: Follows Reddit and RSS feed terms of service

## Maintenance

**Regular tasks**:
- Monitor GitHub Actions runs (weekly)
- Review new posts for quality (weekly)
- Update keyword list as needed (monthly)
- Check for package updates (monthly)

**Automated**:
- Data collection (every 6 hours)
- Database backups (via GitHub artifacts)
- Dependency security scans (GitHub Dependabot)

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| No posts collected | Check Reddit credentials, verify subreddits exist |
| Dashboard blank | Run `collect.py` first to create database |
| GitHub Actions failing | Check secrets are set, review Actions logs |
| SQLite locked | Close dashboard before running `collect.py` |
| Slow dashboard | Clear browser cache, check data volume |

## Cost Analysis

| Service | Cost |
|---------|------|
| **Reddit API** | Free (read-only) |
| **RSS feeds** | Free (public) |
| **Streamlit Cloud** | Free (public repos) |
| **GitHub Actions** | Free (2000 min/month) |
| **Total** | **$0/month** |

Paid alternatives (optional):
- Private GitHub repo: $4/month
- Streamlit Pro: $250/month (unlimited users)
- Dedicated server: $5-20/month

## Roadmap (Future Enhancements)

**Phase 2** (validated MVP):
- Twitter/X integration
- More subreddits (r/Chartered_Accountants, r/IndianStockMarket)
- CA Club forum scraping
- Email digest (weekly summary)

**Phase 3** (scaling):
- ML-based sentiment analysis
- Topic modeling (LDA)
- Anomaly detection (unusual spikes)
- Multi-language support (Hindi, Marathi)

**Phase 4** (product):
- User accounts and saved filters
- Custom dashboards per user
- API for programmatic access
- Slack/Discord integration

## License & Attribution

- **License**: MIT (free for commercial use)
- **Data sources**: Reddit (API), GSTN (RSS), CAClubIndia (RSS)
- **Attribution**: Links back to original posts maintained
- **No warranty**: Use at your own risk

## Getting Started

Choose your path:

1. **Just want to see it?** → [QUICKSTART.md](QUICKSTART.md) (5 min)
2. **Need full setup?** → [SETUP.md](SETUP.md) (30 min)
3. **Want to use it?** → [USAGE.md](USAGE.md) (detailed guide)
4. **Understanding the code?** → You're in the right place!

## Questions?

- Check the docs (QUICKSTART, SETUP, USAGE)
- Review the code (it's well-commented)
- Open an issue on GitHub
- Contact the maintainer

---

**Built for:** Validating compliance automation product-market fit
**Built with:** Python, Streamlit, PRAW, SQLite
**Build time:** ~4 hours
**Time to value:** < 5 minutes
