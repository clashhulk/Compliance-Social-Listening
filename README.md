# India Compliance Pain Tracker (MVP)

A lightweight web app to track and visualize compliance-related discussions from Indian public forums and news sources.

## What it does

- Collects recent posts from Reddit (r/IndiaTax, r/IndiaStartups) and RSS feeds (TaxGuru, Income Tax India)
- Tags content by topic (GST, IncomeTax, TDS, etc.) and pain signals (PortalIssues, Deadlines, Negative sentiment)
- Shows a simple dashboard with trends, top tags, and searchable/filterable posts
- Auto-updates every 6 hours via GitHub Actions

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Reddit API credentials

1. Go to https://www.reddit.com/prefs/apps
2. Create a new app (select "script" type)
3. Copy `.env.example` to `.env`
4. Fill in your credentials in `.env`

### 3. Run initial data collection

```bash
python collect.py
```

This will create a `compliance_data.db` SQLite database with the collected posts.

### 4. Launch the dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser at http://localhost:8501

## Dashboard Features

- **KPIs**: Total posts, unique authors, sources tracked
- **Trend Chart**: Daily mentions over time
- **Top Tags**: Most common compliance topics and pain points
- **Data Table**: Searchable, filterable posts with links to originals
- **CSV Export**: Download filtered results

## Filters

- Date range (default: last 14 days)
- Source (Reddit / RSS)
- Tag contains (comma-separated for OR logic)
- Text search

## Auto-collection with GitHub Actions

The `.github/workflows/collect.yml` runs the collector every 6 hours automatically when deployed to GitHub.

## Stack

- **UI**: Streamlit
- **Data Collection**: PRAW (Reddit), feedparser (RSS)
- **Storage**: SQLite
- **Scheduling**: GitHub Actions
- **Hosting**: Streamlit Community Cloud

## File Structure

```
.
├── app.py                  # Streamlit dashboard
├── collect.py              # Data collection orchestrator
├── src/
│   ├── database.py        # SQLite schema and utilities
│   ├── reddit_collector.py # Reddit data collection
│   ├── rss_collector.py   # RSS feed collection
│   └── tagger.py          # Content tagging logic
├── requirements.txt
├── .env.example
└── README.md
```

## Success Metrics (MVP Goals)

- ≥150 relevant items in 14 days
- ≥40% tagged with pain indicators
- Visible spikes near filing dates
- Reliable 6-hour collection cadence

## License

MIT
