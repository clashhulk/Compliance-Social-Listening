"""
Simple keyword-based tagging for compliance content.
Tags posts by topic and pain indicators.
"""
import re
from typing import List, Set


# Topic keywords
TOPIC_KEYWORDS = {
    'GST': [
        'gst', 'gstr', 'gstin', 'e-invoice', 'einvoice', 'irn', 'e-way bill',
        'eway bill', 'ewaybill', 'input tax credit', 'itc', 'reverse charge'
    ],
    'IncomeTax': [
        'income tax', 'itr', 'return filing', 'tax refund', 'income tax return',
        'advance tax', 'tds refund', '26as', 'form 16'
    ],
    'TDS/TCS': [
        'tds', 'tcs', 'traces', 'form 26q', 'form 27q', 'tds return',
        'tcs return', 'tds certificate', 'tds deduction'
    ],
    'PF/ESI/PT': [
        'pf', 'epfo', 'esic', 'esi', 'provident fund', 'employee state insurance',
        'pt', 'professional tax', 'uan', 'pf return'
    ],
    'MCA/ROC': [
        'mca', 'roc', 'ministry of corporate affairs', 'annual filing',
        'form aoc', 'form mgt', 'dir-3', 'company filing', 'roc filing'
    ],
    'Registration': [
        'registration', 'tan', 'pan', 'din', 'dsc', 'digital signature',
        'udyam', 'msme registration', 'shop act'
    ]
}

# Pain indicator keywords
PAIN_KEYWORDS = {
    'PortalIssues': [
        'portal down', 'portal not working', 'website down', 'server error',
        'login issue', 'login failed', 'otp not received', 'otp issue',
        'captcha', 'session timeout', 'site not working', 'technical issue',
        'system error', 'portal error', 'dsc error', 'token error',
        'authentication failed', 'unable to login', 'cant login', "can't login",
        'portal slow', 'loading error'
    ],
    'Deadlines': [
        'due date', 'deadline', 'last date', 'penalty', 'late fee', 'fine',
        'interest', 'delayed', 'extension', 'missed deadline', 'overdue',
        'filing date', 'expiring', 'expires', 'urgent'
    ],
    'Negative': [
        'error', 'failed', 'failure', 'issue', 'problem', 'bug', 'glitch',
        'annoyed', 'frustrated', 'angry', 'terrible', 'horrible', 'worst',
        'useless', 'pathetic', 'complicated', 'confusing', 'difficult',
        'stuck', 'cant', "can't", 'unable', 'not working', 'broken',
        'rejected', 'delay', 'delayed', 'waiting', 'still waiting'
    ]
}


def normalize_text(text: str) -> str:
    """Normalize text for matching (lowercase, remove extra spaces)."""
    return re.sub(r'\s+', ' ', text.lower()).strip()


def tag_content(title: str, text: str) -> List[str]:
    """
    Tag content based on keywords.
    Returns a list of tags found in the content.
    """
    combined = f"{title} {text}"
    normalized = normalize_text(combined)

    tags: Set[str] = set()

    # Check topic keywords
    for tag, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in normalized:
                tags.add(tag)
                break

    # Check pain keywords
    for tag, keywords in PAIN_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in normalized:
                tags.add(tag)
                break

    return sorted(list(tags))


def has_tag(tags: List[str], search_tags: str) -> bool:
    """
    Check if any of the search tags (comma-separated) exist in the post tags.
    Uses OR logic: returns True if any search tag matches.
    """
    if not search_tags:
        return True

    search_list = [t.strip() for t in search_tags.split(',')]
    return any(tag in tags for tag in search_list)


def is_relevant(title: str, text: str, min_tags: int = 1) -> bool:
    """
    Check if content is relevant based on minimum number of tags.
    Returns True if at least min_tags are found.
    """
    tags = tag_content(title, text)
    return len(tags) >= min_tags
