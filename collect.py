"""
Main collection orchestrator.
Runs all data collectors and manages the database.
"""
import sys
from datetime import datetime

from src.database import init_db, get_stats
from src.reddit_collector import collect_reddit_posts
from src.rss_collector import collect_rss_feeds


def main():
    """Run the complete data collection pipeline."""
    print("\n" + "="*60)
    print("India Compliance Pain Tracker - Data Collection")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Initialize database
    print("Initializing database...")
    init_db()
    print("Database ready.\n")

    # Collect from Reddit
    try:
        reddit_stats = collect_reddit_posts(days_back=14, limit_per_sub=100)
    except Exception as e:
        print(f"Reddit collection failed: {e}")
        reddit_stats = {'total_new': 0, 'total_skipped': 0, 'total_processed': 0}

    # Collect from RSS feeds
    try:
        rss_stats = collect_rss_feeds(days_back=14)
    except Exception as e:
        print(f"RSS collection failed: {e}")
        rss_stats = {'total_new': 0, 'total_skipped': 0, 'total_processed': 0}

    # Get overall database stats
    print("\nFetching database statistics...")
    db_stats = get_stats()

    # Summary report
    print("\n" + "="*60)
    print("COLLECTION COMPLETE")
    print("="*60)
    print(f"\nThis run:")
    print(f"  Reddit: {reddit_stats['total_new']} new posts")
    print(f"  RSS: {rss_stats['total_new']} new entries")
    print(f"  Total new: {reddit_stats['total_new'] + rss_stats['total_new']}")

    print(f"\nDatabase totals:")
    print(f"  Total posts: {db_stats['total_posts']}")
    print(f"  Unique authors: {db_stats['unique_authors']}")
    print(f"  Sources tracked: {db_stats['sources']}")
    if db_stats['earliest_post'] and db_stats['latest_post']:
        print(f"  Date range: {db_stats['earliest_post']} to {db_stats['latest_post']}")

    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")

    # Exit with appropriate code
    if reddit_stats['total_new'] + rss_stats['total_new'] > 0:
        print("Collection successful!")
        sys.exit(0)
    else:
        print("No new posts collected (this may be normal if running frequently).")
        sys.exit(0)


if __name__ == '__main__':
    main()
