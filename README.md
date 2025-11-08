# India Compliance Pain Tracker (MVP)

A lightweight web app to track and visualize compliance-related discussions from Indian public forums and news sources.

## What it does

- Collects recent posts from Reddit (r/IndiaTax, r/IndiaStartups) and RSS feeds (TaxGuru, Income Tax India)
- Tags content by topic (GST, IncomeTax, TDS, etc.) and pain signals (PortalIssues, Deadlines, Negative sentiment)
- Shows a simple dashboard with trends, top tags, and searchable/filterable posts
- Auto-updates every 6 hours via GitHub Actions

## Quick Start

See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

**TL;DR:**
```bash
pip install -r requirements.txt
# Add Reddit credentials to .env
python collect.py
python -m streamlit run app.py
```

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

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[USAGE.md](USAGE.md)** - How to use the dashboard effectively

## Data Sources

- **Reddit**: r/IndiaTax, r/IndiaStartups
- **TaxGuru**: Tax news and compliance updates
- **Income Tax India**: Official government updates

## License

MIT
