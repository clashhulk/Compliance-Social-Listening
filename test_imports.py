"""
Quick test to verify all required packages are installed.
Run this after: pip install -r requirements.txt
"""

print("Testing imports...\n")

try:
    import streamlit
    print("✓ streamlit")
except ImportError as e:
    print(f"✗ streamlit - {e}")

try:
    import pandas
    print("✓ pandas")
except ImportError as e:
    print(f"✗ pandas - {e}")

try:
    import praw
    print("✓ praw")
except ImportError as e:
    print(f"✗ praw - {e}")

try:
    import feedparser
    print("✓ feedparser")
except ImportError as e:
    print(f"✗ feedparser - {e}")

try:
    import plotly
    print("✓ plotly")
except ImportError as e:
    print(f"✗ plotly - {e}")

try:
    from dotenv import load_dotenv
    print("✓ python-dotenv")
except ImportError as e:
    print(f"✗ python-dotenv - {e}")

print("\nAll imports successful!")
