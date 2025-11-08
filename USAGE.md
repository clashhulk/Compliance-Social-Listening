# Usage Guide - India Compliance Pain Tracker

## Running the Application

### Collect Data

Run data collection manually:

```bash
python collect.py
```

This will:
- Fetch recent posts from Reddit (r/IndiaTax, r/IndiaStartups)
- Fetch entries from RSS feeds (GSTN News, CAClubIndia)
- Tag content automatically
- Store in SQLite database
- Display collection summary

**Recommended frequency**: Every 6-12 hours

### View Dashboard

Launch the Streamlit dashboard:

```bash
streamlit run app.py
```

Dashboard URL: http://localhost:8501

## Dashboard Features

### 1. KPI Cards (Top Row)

- **Total Posts**: Number of posts in selected date range
- **Unique Authors**: Distinct authors/sources
- **Sources**: Number of different data sources
- **Pain Signal %**: Percentage of posts with pain indicators (PortalIssues, Deadlines, Negative)

### 2. Visualizations

**Daily Mentions Trend**
- Line chart showing post volume over time
- Hover to see exact counts
- Look for spikes near compliance deadlines (10th, 20th of month)

**Top Tags**
- Bar chart of most common tags
- Red bars = pain indicators (PortalIssues, Deadlines, Negative)
- Blue bars = topic tags (GST, IncomeTax, etc.)

### 3. Filters (Left Sidebar)

**Date Range**
- Default: Last 14 days
- Adjust to see longer/shorter periods
- Useful for before/after deadline analysis

**Source**
- All (default)
- Reddit only
- Specific RSS feeds
- Compare Reddit vs. official news

**Tag Contains**
- Enter comma-separated tags
- OR logic: matches any tag
- Examples:
  - `GST` → All GST posts
  - `GST,PortalIssues` → GST posts OR portal issue posts
  - `Deadlines,Negative` → Deadline or negative sentiment posts

**Text Search**
- Search in title and text content
- Case-insensitive
- Examples:
  - `portal down` → Posts mentioning portal issues
  - `GSTR-1` → Specific GST return
  - `refund delay` → Refund-related complaints

### 4. Posts Table

Searchable, sortable table with:
- Date & time
- Source (Reddit/RSS feed)
- Title snippet
- Tags
- Author
- Score (Reddit upvotes)
- Link to original post

Click column headers to sort.

### 5. CSV Export

Download filtered data as CSV for:
- Further analysis in Excel/Google Sheets
- Reports for stakeholders
- Historical tracking

## Use Cases

### 1. Validate Problem Hypothesis

**Goal**: Prove that GST portal issues are a real, recurring pain point

**Steps**:
1. Set date range to last 30 days
2. Tag filter: `GST,PortalIssues`
3. Check if ≥40% of posts mention pain signals
4. Look for spikes in the trend chart
5. Export CSV for pitch deck

**Success metric**: ≥20 relevant posts with clear pain signals

### 2. Track Deadline Stress

**Goal**: Identify peak stress periods around filing deadlines

**Steps**:
1. Set date range around known deadlines (e.g., 10th-15th of month)
2. Tag filter: `Deadlines,Negative`
3. Compare volume to non-deadline periods
4. Note specific complaints in posts table

**Expected**: 2-3x higher volume around deadlines

### 3. Identify Top Pain Points

**Goal**: Understand what causes the most frustration

**Steps**:
1. Date range: Last 14 days
2. No filters (see all data)
3. Check "Top Tags" chart
4. Focus on red bars (pain indicators)
5. Click through to read actual posts

**Action**: Build features addressing top 3 pain points

### 4. Competitive Intelligence

**Goal**: See what compliance topics are trending

**Steps**:
1. Source filter: "All"
2. Date range: Last 7 days
3. Sort table by Score (Reddit upvotes)
4. Read high-engagement posts
5. Note emerging topics

**Action**: Create content or features for trending topics

### 5. Monitor Specific Compliance Type

**Goal**: Track only Income Tax discussions

**Steps**:
1. Tag filter: `IncomeTax`
2. Text search: Leave empty or add specific terms
3. Review daily trend
4. Export for weekly report

**Use**: Specialized product focus

## Tips & Best Practices

### Getting Quality Insights

1. **Start broad, then narrow**: Use "All" filters first, then drill down
2. **Compare time periods**: Look at week-over-week or month-over-month changes
3. **Read the posts**: Don't just look at charts—click through to understand context
4. **Track patterns**: Note recurring complaints (same error codes, same portal issues)
5. **Correlate with events**: Match spikes to known deadlines or policy changes

### Interpreting the Data

**High volume ≠ always bad**
- Volume spikes near deadlines are expected
- Look for *unexpected* spikes (portal outages, new rules)

**Pain Signal % matters more than volume**
- 20 posts with 80% pain signals > 50 posts with 20% pain signals
- Target: ≥40% pain signals = real, validated problem

**Source matters**
- Reddit = real user frustration
- RSS feeds = official announcements, may lack emotion
- Balance both for full picture

### Updating Data

**Manual collection** (for demos):
```bash
python collect.py
```

**Automated** (production):
- GitHub Actions runs every 6 hours
- Check Actions tab for status
- Database auto-updates

**Before important meetings**:
1. Run `python collect.py` to get latest data
2. Refresh dashboard (F5 or click "Refresh Data" button)
3. Adjust filters to highlight key findings
4. Take screenshots or export CSV

## Example Queries

### Find all GST portal issues this month
- Date range: This month
- Tag filter: `GST,PortalIssues`
- Expected: Multiple posts about login, OTP, timeout issues

### Compare Reddit vs. official news
Run dashboard twice:
1. Source: Reddit → Note volume and pain %
2. Source: GSTN News → Note volume and tone
3. Compare: Reddit usually shows more pain, RSS shows official updates

### Track a specific error
- Text search: `error code 2150` (or whatever error)
- Date range: Last 30 days
- See if it's recurring or one-time issue

### Prepare for investor meeting
1. Date range: Last 14 days (or since last meeting)
2. No filters (show everything)
3. Note total posts, pain %, and top tags
4. Export CSV
5. Prepare 3-4 example posts showing clear pain

## Troubleshooting

**Dashboard shows "No posts found"**
- Run `python collect.py` first
- Check that `compliance_data.db` exists
- Try broader filters (remove tag and text filters)

**Charts not updating**
- Click "Refresh Data" in sidebar
- Restart Streamlit: `Ctrl+C` then `streamlit run app.py`

**CSV export is empty**
- Check that filters aren't too restrictive
- Ensure posts exist in selected date range

**Trend chart is flat**
- May not have enough data yet
- Wait 3-5 days for patterns to emerge
- Try a longer date range

## Advanced Usage

### Custom Tag Taxonomy

Edit [src/tagger.py](src/tagger.py) to add your own keywords and tags.

### Database Queries

Direct SQLite access for power users:

```bash
sqlite3 compliance_data.db
```

Example queries:
```sql
-- Top authors by post count
SELECT author, COUNT(*) as posts
FROM posts
GROUP BY author
ORDER BY posts DESC
LIMIT 10;

-- Posts per day
SELECT DATE(created_at) as date, COUNT(*) as posts
FROM posts
GROUP BY date
ORDER BY date;

-- Most common tags
SELECT tags, COUNT(*) as count
FROM posts
WHERE tags LIKE '%PortalIssues%'
GROUP BY tags
ORDER BY count DESC;
```

### Extending Data Sources

To add more sources:
1. Create a new collector in `src/` (e.g., `twitter_collector.py`)
2. Follow the pattern in `reddit_collector.py`
3. Add to `collect.py` orchestrator
4. Update `README.md` with new source

## Next Steps

Once you're comfortable:
1. Run collection for 2 weeks to establish baseline
2. Set up automated alerts (future feature)
3. Share dashboard URL with team
4. Use data in pitch decks and PRDs
5. Track metrics weekly to validate product-market fit
