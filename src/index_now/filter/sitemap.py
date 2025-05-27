from abc import ABC
from dataclasses import dataclass
from datetime import datetime, timedelta

from .change_frequency import ChangeFrequency


class DateRange(ABC):
    """A date range for filtering sitemap URLs."""

    def __init__(self, start: datetime, end: datetime) -> None:
        self.start: datetime = start
        self.end: datetime = end

    def __repr__(self) -> str:
        return f"DateRange(start={self.start}, end={self.end})"


class Today(DateRange):
    """Today as range for filtering sitemap URLs."""

    def __init__(self) -> None:
        super().__init__(
            start=datetime.now(),
            end=datetime.now(),
        )

    def __repr__(self) -> str:
        return f"Day(today={self.start})"


class Day(DateRange):
    """A specific date for filtering sitemap URLs."""

    def __init__(self, day: datetime) -> None:
        super().__init__(
            start=day,
            end=day,
        )

    def __repr__(self) -> str:
        return f"Day(day={self.start})"


class DaysAgo(DateRange):
    """A number of days ago from today as range for filtering sitemap URLs."""

    def __init__(self, days_ago: int) -> None:
        super().__init__(
            start=datetime.now() - timedelta(days=days_ago),
            end=datetime.now(),
        )
        self.days_ago = days_ago

    def __repr__(self) -> str:
        return f"DaysAgo(days_ago={self.days_ago})"


class LaterThan(DateRange):
    """Period of time after a specific date as range for filtering sitemap URLs."""

    def __init__(self, date: datetime) -> None:
        super().__init__(
            start=date,
            end=datetime.now(),
        )
        self.date = date

    def __repr__(self) -> str:
        return f"LaterThan(date={self.date})"


class EarlierThan(DateRange):
    """Period of time before a specific date as range for filtering sitemap URLs."""

    def __init__(self, date: datetime) -> None:
        super().__init__(
            start=datetime.min,
            end=date,
        )
        self.date = date

    def __repr__(self) -> str:
        return f"EarlierThan(date={self.date})"


@dataclass(slots=True, frozen=True)
class SitemapFilter:
    """Configuration class for filtering sitemap URLs based text, change frequency, date, and more.

    Attributes:
        change_frequency (ChangeFrequency | None): Optional filter for URLs based on change frequency. Ignored by default or if set to `None`.
        date_range (DateRange | None): Optional filter for URLs based on a date range, e.g. `Day`, `DaysAgo`, `LaterThan`, `EarlierThan`, etc. Ignored by default or if set to `None`.
        contains (str | None): Optional filter for URLs. Can be simple string (e.g. `"section1"`) or regular expression (e.g. `r"(section1)|(section2)"`). Ignored by default or if set to `None`.
        excludes (str | None): Optional filter for URLs. Can be simple string (e.g. `"not-include-this"`) or regular expression (e.g. `r"(not-include-this)|(not-include-that)"`). Ignored by default or if set to `None`.
        skip (int | None): Optional number of URLs to be skipped. Ignored by default or if set to `None`.
        take (int | None): Optional limit of URLs to be taken. Ignored by default or if set to `None`.
    """

    change_frequency: ChangeFrequency | None = None
    date_range: DateRange | None = None
    contains: str | None = None
    excludes: str | None = None
    skip: int | None = None
    take: int | None = None
