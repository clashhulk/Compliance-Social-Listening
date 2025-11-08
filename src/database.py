"""
SQLite database setup and utilities for compliance tracking.
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import json


DB_PATH = "compliance_data.db"


def init_db(db_path: str = DB_PATH) -> None:
    """Initialize the SQLite database with required schema."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            title TEXT,
            text TEXT,
            author TEXT,
            url TEXT,
            score INTEGER,
            created_at DATETIME NOT NULL,
            collected_at DATETIME NOT NULL,
            tags TEXT,
            subreddit TEXT
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_created_at ON posts(created_at DESC)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_source ON posts(source)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_tags ON posts(tags)
    """)

    conn.commit()
    conn.close()


def insert_post(
    post_id: str,
    source: str,
    title: str,
    text: str,
    author: str,
    url: str,
    score: int,
    created_at: datetime,
    tags: List[str],
    subreddit: Optional[str] = None,
    db_path: str = DB_PATH
) -> bool:
    """
    Insert a single post into the database.
    Returns True if inserted, False if already exists.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO posts
            (id, source, title, text, author, url, score, created_at, collected_at, tags, subreddit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            post_id,
            source,
            title,
            text,
            author,
            url,
            score,
            created_at,
            datetime.now(),
            json.dumps(tags),
            subreddit
        ))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False


def get_posts(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    source: Optional[str] = None,
    db_path: str = DB_PATH
) -> List[Dict]:
    """
    Retrieve posts from the database with optional filters.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM posts WHERE 1=1"
    params = []

    if start_date:
        query += " AND created_at >= ?"
        params.append(start_date)

    if end_date:
        query += " AND created_at <= ?"
        params.append(end_date)

    if source:
        query += " AND source = ?"
        params.append(source)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    posts = []
    for row in rows:
        post = dict(row)
        post['tags'] = json.loads(post['tags']) if post['tags'] else []
        posts.append(post)

    return posts


def get_stats(db_path: str = DB_PATH) -> Dict:
    """Get basic statistics about the collected data."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM posts")
    total_posts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT author) FROM posts")
    unique_authors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT source) FROM posts")
    sources = cursor.fetchone()[0]

    cursor.execute("SELECT MIN(created_at), MAX(created_at) FROM posts")
    date_range = cursor.fetchone()

    conn.close()

    return {
        'total_posts': total_posts,
        'unique_authors': unique_authors,
        'sources': sources,
        'earliest_post': date_range[0],
        'latest_post': date_range[1]
    }


def post_exists(post_id: str, db_path: str = DB_PATH) -> bool:
    """Check if a post already exists in the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM posts WHERE id = ? LIMIT 1", (post_id,))
    exists = cursor.fetchone() is not None

    conn.close()
    return exists
