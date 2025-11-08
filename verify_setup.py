"""
Setup verification script.
Run this to check if your environment is configured correctly.
"""
import sys
import os
from pathlib import Path


def check_python_version():
    """Check Python version."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor} (need 3.8+)")
        return False


def check_dependencies():
    """Check if required packages are installed."""
    print("\nChecking dependencies...")
    required = ['streamlit', 'pandas', 'praw', 'feedparser', 'plotly', 'dotenv']
    missing = []

    for package in required:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (missing)")
            missing.append(package)

    if missing:
        print(f"\n  Install missing packages: pip install {' '.join(missing)}")
        return False
    return True


def check_env_file():
    """Check if .env file exists and has required variables."""
    print("\nChecking environment configuration...")

    if not Path('.env').exists():
        print("  ✗ .env file not found")
        print("    Run: cp .env.example .env")
        print("    Then add your Reddit API credentials")
        return False

    print("  ✓ .env file exists")

    # Check if .env has credentials
    with open('.env', 'r') as f:
        content = f.read()

    has_id = 'REDDIT_CLIENT_ID' in content and 'your_client_id' not in content
    has_secret = 'REDDIT_CLIENT_SECRET' in content and 'your_secret' not in content

    if has_id and has_secret:
        print("  ✓ Reddit credentials configured")
        return True
    else:
        print("  ⚠ Reddit credentials not set")
        print("    Edit .env and add your Reddit API credentials")
        return False


def check_project_structure():
    """Check if all required files exist."""
    print("\nChecking project structure...")

    required_files = [
        'app.py',
        'collect.py',
        'requirements.txt',
        'src/__init__.py',
        'src/database.py',
        'src/reddit_collector.py',
        'src/rss_collector.py',
        'src/tagger.py',
    ]

    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} (missing)")
            all_exist = False

    return all_exist


def check_database():
    """Check if database can be initialized."""
    print("\nChecking database setup...")

    try:
        from src.database import init_db, DB_PATH
        init_db()

        if Path(DB_PATH).exists():
            print(f"  ✓ Database initialized at {DB_PATH}")
            return True
        else:
            print("  ✗ Database initialization failed")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_reddit_connection():
    """Test Reddit API connection."""
    print("\nTesting Reddit API connection...")

    try:
        from src.reddit_collector import init_reddit
        reddit = init_reddit()
        print("  ✓ Reddit API initialized")

        # Try to fetch one post
        subreddit = reddit.subreddit('IndiaTax')
        post = next(subreddit.new(limit=1))
        print(f"  ✓ Successfully fetched test post from r/IndiaTax")
        return True
    except ValueError as e:
        print(f"  ✗ Configuration error: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Connection error: {e}")
        print("    Check your Reddit credentials and internet connection")
        return False


def test_rss_feeds():
    """Test RSS feed access."""
    print("\nTesting RSS feeds...")

    try:
        import feedparser
        from src.rss_collector import RSS_FEEDS

        success = True
        for name, url in RSS_FEEDS.items():
            feed = feedparser.parse(url)
            if feed.entries:
                print(f"  ✓ {name} ({len(feed.entries)} entries)")
            else:
                print(f"  ⚠ {name} (no entries, may be temporary)")

        return success
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Run all verification checks."""
    print("="*60)
    print("India Compliance Pain Tracker - Setup Verification")
    print("="*60)

    checks = [
        ("Python version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment config", check_env_file),
        ("Project structure", check_project_structure),
        ("Database", check_database),
        ("Reddit API", test_reddit_connection),
        ("RSS feeds", test_rss_feeds),
    ]

    results = {}
    for name, check_func in checks:
        results[name] = check_func()

    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)

    passed = sum(results.values())
    total = len(results)

    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {name}")

    print(f"\nResult: {passed}/{total} checks passed")

    if passed == total:
        print("\n🎉 All checks passed! You're ready to go.")
        print("\nNext steps:")
        print("  1. Run data collection: python collect.py")
        print("  2. Launch dashboard: streamlit run app.py")
        return 0
    else:
        print("\n⚠ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Missing dependencies: pip install -r requirements.txt")
        print("  - Missing .env: cp .env.example .env")
        print("  - Reddit credentials: Edit .env with your API keys")
        return 1


if __name__ == '__main__':
    sys.exit(main())
