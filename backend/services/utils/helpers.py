"""
Helper Utilities

Common helper functions used throughout the application
"""

import re
from datetime import datetime
from urllib.parse import urlparse
from difflib import SequenceMatcher


def clean_text(text):
    """
    Clean and normalize text by removing extra whitespace and special characters

    Args:
        text: Input text

    Returns:
        str: Cleaned text
    """
    if not text:
        return ''

    # Convert to string
    text = str(text)

    # Remove extra whitespace
    text = ' '.join(text.split())

    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def extract_domain(url):
    """
    Extract domain from URL

    Args:
        url: URL string

    Returns:
        str: Domain name or None
    """
    if not url:
        return None

    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        # Remove www. prefix
        domain = domain.replace('www.', '')
        return domain
    except:
        return None


def calculate_match_score(user_interests, prof_interests):
    """
    Calculate match score between user and professor research interests

    Args:
        user_interests: List of user's research interests
        prof_interests: List of professor's research interests

    Returns:
        float: Match score (0-100)
    """
    if not user_interests or not prof_interests:
        return 0.0

    # Convert to lowercase for comparison
    user_set = set([interest.lower() for interest in user_interests])
    prof_set = set([interest.lower() for interest in prof_interests])

    # Calculate exact matches
    exact_matches = len(user_set.intersection(prof_set))

    # Calculate fuzzy matches for remaining items
    fuzzy_score = 0
    matched_prof = set()

    for user_int in user_set:
        best_match = 0
        best_prof = None
        for prof_int in prof_set:
            if prof_int not in matched_prof:
                # Calculate similarity ratio
                ratio = SequenceMatcher(None, user_int, prof_int).ratio()
                if ratio > best_match:
                    best_match = ratio
                    best_prof = prof_int

        if best_match > 0.6:  # Threshold for fuzzy match
            fuzzy_score += best_match
            if best_prof:
                matched_prof.add(best_prof)

    # Combine scores
    total_matches = exact_matches + fuzzy_score
    max_possible = max(len(user_set), len(prof_set))

    if max_possible == 0:
        return 0.0

    # Calculate percentage
    score = (total_matches / max_possible) * 100
    return min(round(score, 2), 100.0)


def format_date(date, format='%Y-%m-%d'):
    """
    Format date object or string to specified format

    Args:
        date: Date object or string
        format: Output format (default: YYYY-MM-DD)

    Returns:
        str: Formatted date string or None
    """
    if not date:
        return None

    try:
        if isinstance(date, str):
            # Try to parse common formats
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d %H:%M:%S']:
                try:
                    date = datetime.strptime(date, fmt)
                    break
                except:
                    continue

        if isinstance(date, datetime):
            return date.strftime(format)

        return None
    except:
        return None


def paginate_query(query, page, per_page):
    """
    Paginate SQLAlchemy query

    Args:
        query: SQLAlchemy query object
        page: Page number (1-indexed)
        per_page: Items per page

    Returns:
        dict: Pagination result with items, total, pages, etc.
    """
    # Get total count
    total = query.count()

    # Calculate pages
    total_pages = (total + per_page - 1) // per_page

    # Get items for current page
    items = query.limit(per_page).offset((page - 1) * per_page).all()

    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_prev': page > 1
    }


def extract_email_from_text(text):
    """
    Extract email addresses from text

    Args:
        text: Input text

    Returns:
        list: List of email addresses found
    """
    if not text:
        return []

    # Email regex pattern
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(pattern, text)

    # Return unique emails
    return list(set(emails))


def truncate_text(text, max_length=100, suffix='...'):
    """
    Truncate text to specified length

    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add when truncated

    Returns:
        str: Truncated text
    """
    if not text:
        return ''

    text = str(text)

    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def get_country_code(country_name):
    """
    Get country code from country name (simple mapping)

    Args:
        country_name: Full country name

    Returns:
        str: 2-letter country code or None
    """
    country_mapping = {
        'united states': 'US',
        'usa': 'US',
        'united kingdom': 'GB',
        'uk': 'GB',
        'canada': 'CA',
        'australia': 'AU',
        'germany': 'DE',
        'france': 'FR',
        'china': 'CN',
        'japan': 'JP',
        'singapore': 'SG',
        'netherlands': 'NL',
        'switzerland': 'CH',
        'sweden': 'SE',
        'norway': 'NO',
        'denmark': 'DK',
        # Add more as needed
    }

    if not country_name:
        return None

    country_name = country_name.lower().strip()
    return country_mapping.get(country_name)
