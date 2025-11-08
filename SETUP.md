# Setup Guide - India Compliance Pain Tracker

## Prerequisites

- Python 3.8 or higher
- Reddit API credentials
- Git (for GitHub Actions deployment)

## Step-by-Step Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Reddit API Credentials

Reddit is the primary data source. You need API credentials:

1. Go to https://www.reddit.com/prefs/apps
2. Scroll down and click "Create App" or "Create Another App"
3. Fill in:
   - **Name**: India Compliance Pain Tracker
   - **App type**: Select "script"
   - **Description**: (optional) Tracking compliance discussions
   - **About URL**: (leave blank)
   - **Redirect URI**: http://localhost:8080 (required but not used)
4. Click "Create app"
5. Note down:
   - **Client ID**: The string under "personal use script"
   - **Client Secret**: The string next to "secret"

### 3. Configure Environment Variables

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your Reddit credentials:

```env
REDDIT_CLIENT_ID=your_actual_client_id
REDDIT_CLIENT_SECRET=your_actual_secret
REDDIT_USER_AGENT=IndiaCompliancePainTracker/1.0
```

### 4. Run Initial Data Collection

```bash
python collect.py
```

This will:
- Create a `compliance_data.db` SQLite database
- Collect recent posts from Reddit and RSS feeds
- Tag and store relevant compliance discussions
- Show a summary of collected data

Expected output:
```
============================================================
India Compliance Pain Tracker - Data Collection
============================================================

Initializing database...
Database ready.

Initializing Reddit API...

Collecting from r/IndiaTax...
  Processed: 100, New: 25, Skipped: 75
...
```

### 5. Launch the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser at http://localhost:8501

## Deployment to Streamlit Community Cloud

### Prerequisites
- GitHub account
- Streamlit Community Cloud account (free at https://share.streamlit.io/)

### Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/compliance-tracker.git
   git push -u origin main
   ```

2. **Set up GitHub Secrets** (for automated collection)
   - Go to your GitHub repo → Settings → Secrets and variables → Actions
   - Add secrets:
     - `REDDIT_CLIENT_ID`: Your Reddit client ID
     - `REDDIT_CLIENT_SECRET`: Your Reddit client secret

3. **Deploy to Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Select your GitHub repository
   - Main file path: `app.py`
   - Advanced settings → Secrets:
     ```toml
     REDDIT_CLIENT_ID = "your_client_id"
     REDDIT_CLIENT_SECRET = "your_client_secret"
     REDDIT_USER_AGENT = "IndiaCompliancePainTracker/1.0"
     ```
   - Click "Deploy"

4. **Enable GitHub Actions**
   - The workflow in `.github/workflows/collect.yml` will run every 6 hours
   - It will download the existing database, collect new data, and upload the updated database
   - You can also trigger it manually from the Actions tab

## Troubleshooting

### "Reddit credentials not found" error
- Make sure you created the `.env` file
- Check that the credentials are correct
- Ensure no extra spaces in the `.env` file

### No posts collected
- This is normal if you run collection frequently
- Reddit has rate limits; wait a few minutes between runs
- Check that the subreddits (r/IndiaTax, r/IndiaStartups) exist and are public

### Database locked error
- Close the Streamlit dashboard before running `collect.py`
- SQLite doesn't handle concurrent writes well

### GitHub Actions not running
- Check that secrets are set correctly
- Look at the Actions tab for error logs
- First run needs manual trigger to create the database artifact

### RSS feeds not loading
- Some feeds may be temporarily unavailable
- Check the URLs in `src/rss_collector.py`
- Collection will continue even if one feed fails

## Testing the Setup

Run a quick test collection:

```bash
python -c "from src.database import init_db; init_db(); print('Database initialized successfully')"
python -c "from src.rss_collector import collect_rss_feeds; collect_rss_feeds(days_back=7)"
```

Then check the dashboard:
```bash
streamlit run app.py
```

## Next Steps

Once setup is complete:
1. Let it run for 2-3 days to accumulate data
2. Check the dashboard daily for trends
3. Adjust filters to find specific pain signals
4. Export data as CSV for further analysis
5. Monitor GitHub Actions runs to ensure collection is working

## Support

For issues or questions:
- Check the main [README.md](README.md)
- Review error messages in the terminal
- Check GitHub Actions logs for automated collection issues
