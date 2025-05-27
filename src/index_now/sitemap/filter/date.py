from datetime import datetime


def get_complete_date(date: datetime) -> str:
    """Get a complete date string in the format YYYY-MM-DD."""

    return date.strftime("%Y-%m-%d")
