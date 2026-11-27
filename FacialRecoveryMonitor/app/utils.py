"""Formatting and small helpers shared by pages."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Optional

from .database import parse_iso

RANGE_OPTIONS = {"All time": None, "Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}


def since_for_range(label: str) -> Optional[str]:
    days = RANGE_OPTIONS.get(label)
    if days is None:
        return None
    start = datetime.combine(date.today() - timedelta(days=days - 1), datetime.min.time())
    return start.isoformat()


def fmt_date(value: str | datetime | None, default: str = "—") -> str:
    dt = parse_iso(value) if isinstance(value, str) else value
    return dt.strftime("%d %b %Y").lstrip("0") if dt else default


def fmt_time(value: str | datetime | None) -> str:
    dt = parse_iso(value) if isinstance(value, str) else value
    return dt.strftime("%H:%M") if dt else ""


def fmt_datetime(value: str | datetime | None, default: str = "—") -> str:
    dt = parse_iso(value) if isinstance(value, str) else value
    return f"{fmt_date(dt)} · {fmt_time(dt)}" if dt else default


def relative_day(value: str | None) -> str:
    dt = parse_iso(value)
    if not dt:
        return ""
    delta = (date.today() - dt.date()).days
    if delta == 0:
        return "Today"
    if delta == 1:
        return "Yesterday"
    if delta < 0:
        return fmt_date(dt)
    return f"{delta} days ago"


def long_today() -> str:
    d = date.today()
    return f"{d.strftime('%A')}, {d.day} {d.strftime('%B %Y')}"


def tracking_duration(first: str | None, last: str | None) -> tuple[str, str]:
    """Return (value, caption) describing the span between first and latest records."""
    a, b = parse_iso(first), parse_iso(last)
    if not a or not b:
        return "—", "No records yet"
    days = (b.date() - a.date()).days + 1
    value = f"{days} day" + ("" if days == 1 else "s")
    return value, f"{fmt_date(a)} → {fmt_date(b)}"


def plural(n: int, word: str, suffix: str = "s") -> str:
    return f"{n} {word}{'' if n == 1 else suffix}"


def validate_date(text: str) -> tuple[bool, str]:
    """Validate an optional YYYY-MM-DD date that must not be in the future."""
    text = (text or "").strip()
    if not text:
        return True, ""
    try:
        d = datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return False, "Please enter the date as YYYY-MM-DD, for example 2026-03-14."
    if d > date.today():
        return False, "The tracking start date cannot be in the future."
    if d.year < 1900:
        return False, "Please enter a realistic date."
    return True, ""
