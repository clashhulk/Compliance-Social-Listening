"""
India Compliance Pain Tracker - Streamlit Dashboard
Simple, fast, actionable compliance intelligence.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

from src.database import get_posts, get_stats, init_db, DB_PATH
import os


# Page config
st.set_page_config(
    page_title="India Compliance Pain Tracker",
    page_icon="📊",
    layout="wide"
)


# Initialize database if it doesn't exist
if not os.path.exists(DB_PATH):
    st.warning("Database not found. Run `python collect.py` to collect data first.")
    st.stop()

init_db()


# Title and description
st.title("📊 India Compliance Pain Tracker")
st.markdown("**Real-time tracking of compliance pain signals from public forums and news sources**")
st.divider()


# Sidebar filters
with st.sidebar:
    st.header("Filters")

    # Date range
    st.subheader("Date Range")
    default_start = datetime.now() - timedelta(days=14)
    default_end = datetime.now()

    date_range = st.date_input(
        "Select dates",
        value=(default_start, default_end),
        max_value=datetime.now()
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = date_range[0]
        end_date = datetime.now()

    # Source filter
    st.subheader("Source")
    source_filter = st.selectbox(
        "Select source",
        options=["All", "Reddit", "GSTN News", "CAClubIndia Tax"]
    )

    # Tag filter
    st.subheader("Tags")
    tag_filter = st.text_input(
        "Tag contains (comma = OR)",
        placeholder="e.g., GST, PortalIssues"
    )

    # Text search
    st.subheader("Text Search")
    text_filter = st.text_input(
        "Search in title/text",
        placeholder="e.g., portal down"
    )

    st.divider()

    # Refresh button
    if st.button("🔄 Refresh Data"):
        st.rerun()


# Fetch data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data(start, end, source):
    """Load posts from database with caching."""
    posts = get_posts(
        start_date=datetime.combine(start, datetime.min.time()),
        end_date=datetime.combine(end, datetime.max.time()),
        source=None if source == "All" else source
    )
    return posts


# Load posts
posts = load_data(start_date, end_date, source_filter)

# Convert to DataFrame
if posts:
    df = pd.DataFrame(posts)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['date'] = df['created_at'].dt.date

    # Apply tag filter
    if tag_filter:
        search_tags = [t.strip() for t in tag_filter.split(',')]
        df = df[df['tags'].apply(
            lambda tags: any(tag in tags for tag in search_tags)
        )]

    # Apply text filter
    if text_filter:
        mask = (
            df['title'].str.contains(text_filter, case=False, na=False) |
            df['text'].str.contains(text_filter, case=False, na=False)
        )
        df = df[mask]
else:
    df = pd.DataFrame()


# KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Posts", len(df))

with col2:
    unique_authors = df['author'].nunique() if not df.empty else 0
    st.metric("Unique Authors", unique_authors)

with col3:
    unique_sources = df['source'].nunique() if not df.empty else 0
    st.metric("Sources", unique_sources)

with col4:
    if not df.empty:
        all_tags = []
        for tags in df['tags']:
            all_tags.extend(tags)
        pain_tags = ['PortalIssues', 'Deadlines', 'Negative']
        pain_count = sum(1 for tag in all_tags if tag in pain_tags)
        total_tags = len(all_tags)
        pain_pct = (pain_count / total_tags * 100) if total_tags > 0 else 0
        st.metric("Pain Signal %", f"{pain_pct:.1f}%")
    else:
        st.metric("Pain Signal %", "0%")

st.divider()


# Charts section
if not df.empty:
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📈 Daily Mentions Trend")

        # Daily counts
        daily_counts = df.groupby('date').size().reset_index(name='count')
        daily_counts['date'] = pd.to_datetime(daily_counts['date'])

        fig_trend = px.line(
            daily_counts,
            x='date',
            y='count',
            markers=True,
            labels={'date': 'Date', 'count': 'Posts'}
        )
        fig_trend.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            hovermode='x unified'
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_right:
        st.subheader("🏷️ Top Tags")

        # Count tags
        all_tags = []
        for tags in df['tags']:
            all_tags.extend(tags)

        if all_tags:
            tag_counts = pd.Series(all_tags).value_counts().head(10)

            # Color coding for pain tags
            colors = ['#ff6b6b' if tag in ['PortalIssues', 'Deadlines', 'Negative']
                     else '#4ecdc4' for tag in tag_counts.index]

            fig_tags = go.Figure([go.Bar(
                x=tag_counts.values,
                y=tag_counts.index,
                orientation='h',
                marker_color=colors
            )])
            fig_tags.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                yaxis={'categoryorder': 'total ascending'},
                xaxis_title="Count",
                yaxis_title=""
            )
            st.plotly_chart(fig_tags, use_container_width=True)
        else:
            st.info("No tags found in filtered data.")

    st.divider()

    # Data table
    st.subheader("📋 Posts Table")

    # Prepare display DataFrame
    display_df = df.copy()
    display_df['tags'] = display_df['tags'].apply(lambda x: ', '.join(x) if x else '')
    display_df['snippet'] = display_df.apply(
        lambda row: (row['title'][:100] + '...') if len(row['title']) > 100
        else row['title'], axis=1
    )

    # Select columns to display
    display_cols = ['created_at', 'source', 'snippet', 'tags', 'author', 'score', 'url']
    table_df = display_df[display_cols].copy()
    table_df = table_df.sort_values('created_at', ascending=False)

    # Format datetime
    table_df['created_at'] = table_df['created_at'].dt.strftime('%Y-%m-%d %H:%M')

    # Display with pagination
    st.dataframe(
        table_df,
        column_config={
            "created_at": "Date",
            "source": "Source",
            "snippet": "Title",
            "tags": "Tags",
            "author": "Author",
            "score": "Score",
            "url": st.column_config.LinkColumn("Link", display_text="View")
        },
        hide_index=True,
        use_container_width=True,
        height=400
    )

    # Export button
    st.divider()

    # Prepare export data
    export_df = df.copy()
    export_df['tags'] = export_df['tags'].apply(lambda x: ', '.join(x) if x else '')
    export_cols = ['created_at', 'source', 'title', 'text', 'author', 'score', 'url', 'tags']
    export_df = export_df[export_cols]

    csv = export_df.to_csv(index=False)

    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"compliance_posts_{start_date}_to_{end_date}.csv",
        mime="text/csv"
    )

else:
    st.info("No posts found matching the selected filters. Try adjusting your filters or run `python collect.py` to collect data.")


# Footer
st.divider()
st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Data source: Reddit & RSS feeds")
