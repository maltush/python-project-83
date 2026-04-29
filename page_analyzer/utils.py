from typing import Optional


def truncate(text: Optional[str], n: int = 200) -> Optional[str]:
    """Truncate text to n characters and append '...' if trimmed."""
    if text is None:
        return None
    return text if len(text) <= n else text[:n] + "..."
