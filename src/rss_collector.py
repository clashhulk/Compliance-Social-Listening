"""
RSS feed collector for compliance news and updates.
Collects from GSTN News and CAClubIndia Tax News.
"""
from datetime import datetime, timedelta
from typing import List, Dict
import feedparser
import hashlib

from .tagger import tag_content, is_relevant
from .database import insert_post, post_exists


# RSS feeds to monitor
RSS_FEEDS = {
    'TaxGuru': 'https://taxguru.in/feed',
    'Income Tax India': 'https://incometaxindia.gov.in/_layouts/15/Dit/Pages/Rss.aspx?List=Latest+Tax+Updates',
    'SEBI': 'https://www.sebi.gov.in/sebirss.xml'
}


def generate_post_id(url: str, title: str) -> str:
    """Generate a unique post ID from URL and title."""
    content = f"{url}{title}"
    hash_object = hashlib.md5(content.encode())
    return f"rss_{hash_object.hexdigest()}"


def collect_from_feed(
    feed_name: str,
    feed_url: str,
    days_back: int = 14
) -> Dict[str, int]:
    """
    Collect entries from a single RSS feed.
    Returns stats: new, skipped, total
    """
    stats = {'new': 0, 'skipped': 0, 'total': 0, 'errors': 0}

    try:
        print(f"  Fetching {feed_name}...")
        feed = feedparser.parse(feed_url)

        if feed.bozo:
            print(f"  Warning: Feed parsing issue for {feed_name}")

        cutoff_date = datetime.now() - timedelta(days=days_back)

        for entry in feed.entries:
            stats['total'] += 1

            # Extract published date
            published = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                published = datetime(*entry.updated_parsed[:6])
            else:
                # If no date, assume it's recent
                published = datetime.now()

            # Skip if too old
            if published < cutoff_date:
                continue

            # Extract fields
            title = entry.get('title', '').strip()
            summary = entry.get('summary', '') or entry.get('description', '')
            link = entry.get('link', '')

            # Generate unique ID
            post_id = generate_post_id(link, title)

            # Skip if already in DB
            if post_exists(post_id):
                stats['skipped'] += 1
                continue

            # Check relevance
            if not is_relevant(title, summary, min_tags=1):
                stats['skipped'] += 1
                continue

            # Tag the content
            tags = tag_content(title, summary)

            # Add SEBI-specific tags based on URL path
            if feed_name == 'SEBI':
                tags.append('SEBI')  # Always tag SEBI posts with SEBI
                # Add document type tags based on URL path
                link_lower = link.lower()
                if '/press-releases/' in link_lower or '/media-and-notifications/press-releases/' in link_lower:
                    tags.append('PressRelease')
                elif '/circulars/' in link_lower or '/legal/circulars/' in link_lower:
                    tags.append('Circular')
                elif '/orders/' in link_lower or '/legal/orders/' in link_lower or '/enforcement/orders/' in link_lower:
                    tags.append('Order')
                elif '/regulations/' in link_lower or '/legal/regulations/' in link_lower:
                    tags.append('Regulation')
                elif '/enforcement/' in link_lower:
                    tags.append('Enforcement')
                # Remove duplicates and sort
                tags = sorted(list(set(tags)))

            # Extract author
            author = entry.get('author', feed_name)

            # Insert into database
            success = insert_post(
                post_id=post_id,
                source=feed_name,
                title=title,
                text=summary,
                author=author,
                url=link,
                score=0,  # RSS feeds don't have scores
                created_at=published,
                tags=tags,
                subreddit=None
            )

            if success:
                stats['new'] += 1
            else:
                stats['skipped'] += 1

    except Exception as e:
        print(f"  Error collecting from {feed_name}: {e}")
        stats['errors'] += 1

    return stats


def collect_rss_feeds(days_back: int = 14) -> Dict[str, any]:
    """
    Main function to collect from all RSS feeds.
    Returns overall statistics.
    """
    print("Collecting from RSS feeds...")

    overall_stats = {
        'total_new': 0,
        'total_skipped': 0,
        'total_processed': 0,
        'feeds': {}
    }

    for feed_name, feed_url in RSS_FEEDS.items():
        stats = collect_from_feed(feed_name, feed_url, days_back)

        print(f"  {feed_name}: Processed: {stats['total']}, New: {stats['new']}, Skipped: {stats['skipped']}")

        overall_stats['total_new'] += stats['new']
        overall_stats['total_skipped'] += stats['skipped']
        overall_stats['total_processed'] += stats['total']
        overall_stats['feeds'][feed_name] = stats

    print(f"\n{'='*50}")
    print(f"RSS Collection Summary:")
    print(f"  Total processed: {overall_stats['total_processed']}")
    print(f"  New posts added: {overall_stats['total_new']}")
    print(f"  Skipped: {overall_stats['total_skipped']}")
    print(f"{'='*50}\n")

    return overall_stats


if __name__ == '__main__':
    # For testing
    from database import init_db
    init_db()
    collect_rss_feeds()
