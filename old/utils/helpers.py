import re


def clean_text(text):
    """Remove line breaks, extra spaces, and special characters from text."""
    text = re.sub(r'\s+', ' ', text).strip()
    return text
