"""
Date and time utilities for FirstMile Deals system.
Provides consistent date handling across all scripts.
"""
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple


def days_since(date_str: Optional[str]) -> int:
    """
    Calculate days since a given date string.

    Args:
        date_str: ISO format date string (e.g., '2025-10-01T12:00:00Z')

    Returns:
        Number of days since date, or 999 if invalid/missing

    Examples:
        >>> days_since('2025-10-01T00:00:00Z')
        9  # If today is 2025-10-10
        >>> days_since(None)
        999
        >>> days_since('invalid')
        999
    """
    if not date_str:
        return 999

    try:
        # Handle ISO format with or without timezone
        if 'Z' in date_str:
            date_str = date_str.replace('Z', '+00:00')

        date = datetime.fromisoformat(date_str)

        # Make timezone-aware if needed
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        delta = now - date

        return delta.days

    except (ValueError, AttributeError, TypeError):
        return 999


def days_until(date_str: Optional[str]) -> int:
    """
    Calculate days until a given date string.

    Args:
        date_str: ISO format date string

    Returns:
        Number of days until date (negative if past), or 999 if invalid/missing
    """
    if not date_str:
        return 999

    try:
        if 'Z' in date_str:
            date_str = date_str.replace('Z', '+00:00')

        date = datetime.fromisoformat(date_str)

        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        delta = date - now

        return delta.days

    except (ValueError, AttributeError, TypeError):
        return 999


def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """
    Parse date string to datetime object.

    Args:
        date_str: Date string in various formats

    Returns:
        datetime object or None if invalid
    """
    if not date_str:
        return None

    try:
        # Handle ISO format
        if 'T' in date_str:
            if 'Z' in date_str:
                date_str = date_str.replace('Z', '+00:00')
            date = datetime.fromisoformat(date_str)
        else:
            # Try common date formats
            for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
                try:
                    date = datetime.strptime(date_str, fmt)
                    break
                except ValueError:
                    continue
            else:
                return None

        # Make timezone-aware if needed
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)

        return date

    except (ValueError, AttributeError, TypeError):
        return None


def format_date(date: Optional[datetime], format_str: str = '%Y-%m-%d') -> str:
    """
    Format datetime object to string.

    Args:
        date: datetime object
        format_str: Format string (default: YYYY-MM-DD)

    Returns:
        Formatted date string or empty string if None
    """
    if date is None:
        return ''

    try:
        return date.strftime(format_str)
    except (ValueError, AttributeError):
        return ''


def get_timestamp_ms() -> int:
    """
    Get current Unix timestamp in milliseconds (for HubSpot API).

    Returns:
        Current timestamp in milliseconds
    """
    return int(time.time() * 1000)


def is_business_day(date: datetime) -> bool:
    """
    Check if date is a business day (Monday-Friday).

    Args:
        date: datetime object

    Returns:
        True if business day, False if weekend
    """
    return date.weekday() < 5  # Monday = 0, Sunday = 6


def add_business_days(date: datetime, days: int) -> datetime:
    """
    Add business days to a date (skipping weekends).

    Args:
        date: Starting date
        days: Number of business days to add

    Returns:
        New date after adding business days
    """
    current = date
    added = 0

    while added < days:
        current += timedelta(days=1)
        if is_business_day(current):
            added += 1

    return current


def calculate_sla_status(
    ship_date: Optional[str],
    delivery_date: Optional[str],
    sla_window: int
) -> Tuple[bool, int]:
    """
    Calculate SLA compliance status.

    Args:
        ship_date: Ship date string
        delivery_date: Delivery date string
        sla_window: SLA window in days

    Returns:
        Tuple of (within_sla: bool, transit_days: int)

    Examples:
        >>> calculate_sla_status('2025-10-01', '2025-10-04', 5)
        (True, 3)
        >>> calculate_sla_status('2025-10-01', '2025-10-08', 5)
        (False, 7)
    """
    if not ship_date or not delivery_date:
        return (False, 999)

    ship = parse_date(ship_date)
    delivery = parse_date(delivery_date)

    if ship is None or delivery is None:
        return (False, 999)

    transit_days = (delivery - ship).days

    within_sla = transit_days <= sla_window

    return (within_sla, transit_days)


def get_age_category(days: int) -> str:
    """
    Categorize age into human-readable buckets.

    Args:
        days: Number of days

    Returns:
        Age category string

    Examples:
        >>> get_age_category(3)
        'Fresh (0-7 days)'
        >>> get_age_category(25)
        'Aging (15-30 days)'
        >>> get_age_category(100)
        'Stale (90+ days)'
    """
    if days <= 7:
        return 'Fresh (0-7 days)'
    elif days <= 14:
        return 'Recent (8-14 days)'
    elif days <= 30:
        return 'Aging (15-30 days)'
    elif days <= 60:
        return 'Old (31-60 days)'
    elif days <= 90:
        return 'Very Old (61-90 days)'
    else:
        return 'Stale (90+ days)'


def format_age_display(days: int) -> str:
    """
    Format age for display with appropriate units.

    Args:
        days: Number of days

    Returns:
        Formatted string

    Examples:
        >>> format_age_display(3)
        '3d'
        >>> format_age_display(45)
        '45d (6w)'
        >>> format_age_display(120)
        '120d (4mo)'
    """
    if days >= 365:
        years = days // 365
        return f"{days}d ({years}y)"
    elif days >= 30:
        months = days // 30
        return f"{days}d ({months}mo)"
    elif days >= 7:
        weeks = days // 7
        return f"{days}d ({weeks}w)"
    else:
        return f"{days}d"


# Import time for timestamp function
import time
