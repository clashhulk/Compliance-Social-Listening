"""
Reddit data collector using PRAW.
Collects posts from specified subreddits based on compliance keywords.
"""
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import praw
from dotenv import load_dotenv

from .tagger import tag_content, is_relevant
from .database import insert_post, post_exists


# Target subreddits
TARGET_SUBREDDITS = ['IndiaTax', 'IndiaStartups']

# Search keywords for relevance
SEARCH_KEYWORDS = [
    'GST', 'GSTR', 'e-invoice', 'IRN', 'e-way bill', 'ITR', 'income tax',
    'refund', 'TDS', 'TRACES', 'PF', 'EPFO', 'ESIC', 'MCA', 'ROC',
    'due date', 'penalty', 'portal', 'error', 'compliance', 'filing'
]


def init_reddit() -> praw.Reddit:
    """Initialize Reddit API client."""
    load_dotenv()

    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    user_agent = os.getenv('REDDIT_USER_AGENT', 'IndiaCompliancePainTracker/1.0')

    if not client_id or not client_secret:
        raise ValueError(
            "Reddit credentials not found. Please set REDDIT_CLIENT_ID and "
            "REDDIT_CLIENT_SECRET in .env file"
        )

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )


def collect_from_subreddit(
    reddit: praw.Reddit,
    subreddit_name: str,
    days_back: int = 14,
    limit: int = 100
) -> Dict[str, int]:
    """
    Collect posts from a single subreddit.
    Returns stats: new, skipped, total
    """
    subreddit = reddit.subreddit(subreddit_name)
    cutoff_date = datetime.now() - timedelta(days=days_back)

    stats = {'new': 0, 'skipped': 0, 'total': 0}

    try:
        # Get recent posts (sort by new)
        for submission in subreddit.new(limit=limit):
            stats['total'] += 1

            created_time = datetime.fromtimestamp(submission.created_utc)

            # Skip if too old
            if created_time < cutoff_date:
                continue

            # Build post ID
            post_id = f"reddit_{submission.id}"

            # Skip if already in DB
            if post_exists(post_id):
                stats['skipped'] += 1
                continue

            # Extract text
            title = submission.title or ""
            text = submission.selftext or ""

            # Check relevance
            if not is_relevant(title, text, min_tags=1):
                stats['skipped'] += 1
                continue

            # Tag the content
            tags = tag_content(title, text)

            # Insert into database
            success = insert_post(
                post_id=post_id,
                source='Reddit',
                title=title,
                text=text,
                author=str(submission.author) if submission.author else '[deleted]',
                url=f"https://reddit.com{submission.permalink}",
                score=submission.score,
                created_at=created_time,
                tags=tags,
                subreddit=subreddit_name
            )

            if success:
                stats['new'] += 1
            else:
                stats['skipped'] += 1

    except Exception as e:
        print(f"Error collecting from r/{subreddit_name}: {e}")

    return stats


def collect_reddit_posts(days_back: int = 14, limit_per_sub: int = 100) -> Dict[str, any]:
    """
    Main function to collect posts from all target subreddits.
    Returns overall statistics.
    """
    print("Initializing Reddit API...")
    reddit = init_reddit()

    overall_stats = {
        'total_new': 0,
        'total_skipped': 0,
        'total_processed': 0,
        'subreddits': {}
    }

    for subreddit_name in TARGET_SUBREDDITS:
        print(f"\nCollecting from r/{subreddit_name}...")
        stats = collect_from_subreddit(reddit, subreddit_name, days_back, limit_per_sub)

        print(f"  Processed: {stats['total']}, New: {stats['new']}, Skipped: {stats['skipped']}")

        overall_stats['total_new'] += stats['new']
        overall_stats['total_skipped'] += stats['skipped']
        overall_stats['total_processed'] += stats['total']
        overall_stats['subreddits'][subreddit_name] = stats

    print(f"\n{'='*50}")
    print(f"Reddit Collection Summary:")
    print(f"  Total processed: {overall_stats['total_processed']}")
    print(f"  New posts added: {overall_stats['total_new']}")
    print(f"  Skipped: {overall_stats['total_skipped']}")
    print(f"{'='*50}\n")

    return overall_stats


if __name__ == '__main__':
    # For testing
    from database import init_db
    init_db()
    collect_reddit_posts()
