"""
Utility functions for the AgentMail system
"""

from typing import List, Dict, Any
import re


def extract_email_addresses(text: str) -> List[str]:
    """
    Extract email addresses from text.

    Args:
        text: Text to search for email addresses

    Returns:
        List of email addresses found
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, text)


def count_questions(text: str) -> int:
    """
    Count the number of questions in a text.

    Args:
        text: Text to analyze

    Returns:
        Number of questions found
    """
    return text.count('?')


def detect_urgency(text: str) -> Dict[str, Any]:
    """
    Detect urgency indicators in text.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with urgency information
    """
    urgency_keywords = {
        'high': ['urgent', 'asap', 'immediately', 'critical', 'emergency'],
        'medium': ['soon', 'quickly', 'priority', 'important'],
        'low': ['when you can', 'no rush', 'whenever'],
    }

    text_lower = text.lower()
    detected = {
        'level': 'normal',
        'indicators': [],
    }

    for level, keywords in urgency_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected['indicators'].append(keyword)
                if level == 'high':
                    detected['level'] = 'high'
                elif level == 'medium' and detected['level'] != 'high':
                    detected['level'] = 'medium'

    return detected


def sanitize_text(text: str) -> str:
    """
    Sanitize text by removing potentially problematic characters.

    Args:
        text: Text to sanitize

    Returns:
        Sanitized text
    """
    # Remove null bytes
    text = text.replace('\x00', '')

    # Normalize whitespace
    text = ' '.join(text.split())

    return text


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to append if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def format_email_response(
    greeting: str,
    body: str,
    closing: str,
    sender_name: str
) -> str:
    """
    Format an email response with proper structure.

    Args:
        greeting: Opening greeting
        body: Main content
        closing: Closing phrase
        sender_name: Name of sender

    Returns:
        Formatted email string
    """
    parts = [
        f"{greeting},",
        "",
        body,
        "",
        f"{closing},",
        sender_name
    ]

    return "\n".join(parts)
