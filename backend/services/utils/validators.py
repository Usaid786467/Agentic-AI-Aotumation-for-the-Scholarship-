"""
Input Validation Utilities

Provides validation functions for various input types
"""

import re
from datetime import datetime
from urllib.parse import urlparse


def validate_email(email):
    """
    Validate email address format

    Args:
        email: Email address string

    Returns:
        bool: True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False

    # Email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url):
    """
    Validate URL format

    Args:
        url: URL string

    Returns:
        bool: True if valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def validate_date(date_str, format='%Y-%m-%d'):
    """
    Validate date string format

    Args:
        date_str: Date string
        format: Expected date format (default: YYYY-MM-DD)

    Returns:
        bool: True if valid, False otherwise
    """
    if not date_str or not isinstance(date_str, str):
        return False

    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False


def validate_required_fields(data, required_fields):
    """
    Validate that required fields are present in data

    Args:
        data: Dictionary to validate
        required_fields: List of required field names

    Returns:
        tuple: (is_valid, missing_fields)
    """
    if not isinstance(data, dict):
        return False, required_fields

    missing = [field for field in required_fields if field not in data or not data[field]]
    return len(missing) == 0, missing


def sanitize_string(text, max_length=None):
    """
    Sanitize string input by removing potentially harmful characters

    Args:
        text: Input text
        max_length: Maximum allowed length (optional)

    Returns:
        str: Sanitized text
    """
    if not text:
        return ''

    # Convert to string
    text = str(text)

    # Remove null bytes
    text = text.replace('\x00', '')

    # Trim whitespace
    text = text.strip()

    # Limit length if specified
    if max_length and len(text) > max_length:
        text = text[:max_length]

    return text


def validate_file_extension(filename, allowed_extensions):
    """
    Validate file extension

    Args:
        filename: File name
        allowed_extensions: Set of allowed extensions (e.g., {'pdf', 'doc'})

    Returns:
        bool: True if valid, False otherwise
    """
    if not filename or '.' not in filename:
        return False

    ext = filename.rsplit('.', 1)[1].lower()
    return ext in allowed_extensions
