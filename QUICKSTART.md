# Quick Start - 5 Minutes to Dashboard

Get the India Compliance Pain Tracker running in 5 minutes.

## Step 1: Install (1 min)

```bash
pip install -r requirements.txt
```

## Step 2: Configure Reddit API (2 min)

1. Visit https://www.reddit.com/prefs/apps
2. Click "Create App" → Select "script"
3. Note your Client ID and Secret

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_secret_here
REDDIT_USER_AGENT=IndiaCompliancePainTracker/1.0
```

## Step 3: Collect Data (1 min)

```bash
python collect.py
```

Wait for it to finish. You should see:
```
============================================================
COLLECTION COMPLETE
============================================================
```

## Step 4: Launch Dashboard (1 min)

```bash
streamlit run app.py
```

Dashboard opens at http://localhost:8501

## That's it!

You should see:
- Total posts collected
- Daily trend chart
- Top tags (topics and pain points)
- Searchable table of posts

## What to Check

**Success metrics** (for MVP validation):
- ≥150 posts in 14 days ✓
- ≥40% with pain signals (PortalIssues, Deadlines, Negative) ✓
- Visible spikes in trend chart ✓

**If you see "No posts found"**:
- Make sure `collect.py` finished successfully
- Check that `compliance_data.db` exists in the folder
- Try running `collect.py` again

## Next Steps

1. **Run daily**: `python collect.py` every day for a week
2. **Explore filters**: Use date range, tags, and search in the sidebar
3. **Export data**: Click "Download as CSV" for reports
4. **Deploy**: Follow [SETUP.md](SETUP.md) to deploy on Streamlit Cloud with auto-collection

## Common Issues

**"Reddit credentials not found"**
- Check your `.env` file exists
- Make sure credentials are correct (no extra spaces)

**"No new posts collected"**
- Normal if running frequently (Reddit rate limits)
- Wait a few hours and try again
- RSS feeds may be slow to update

**Dashboard is slow**
- First load takes a few seconds (normal)
- Cached after first view
- More data = slightly slower (still fast)

## Get Help

- Detailed setup: [SETUP.md](SETUP.md)
- Usage guide: [USAGE.md](USAGE.md)
- Main docs: [README.md](README.md)

---

**Built with:** Streamlit + PRAW + SQLite
**Time to value:** < 5 minutes
**Data refresh:** Every 6 hours (automated)
