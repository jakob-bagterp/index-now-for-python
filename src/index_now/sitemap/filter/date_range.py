from abc import ABC
from datetime import datetime, timedelta


class DateRange(ABC):
    """A date range for filtering sitemap URLs."""

    __slots__ = ["start", "end"]

    def __init__(self, start: datetime, end: datetime) -> None:
        self.start: datetime = start
        self.end: datetime = end

    def __repr__(self) -> str:
        return f"DateRange(start={self.start}, end={self.end})"

    def is_within_range(self, date: datetime) -> bool:
        """Check if a given date is within the date range."""

        return self.start.date() <= date.date() <= self.end.date()


class Today(DateRange):
    """Today as range for filtering sitemap URLs."""

    def __init__(self) -> None:
        super().__init__(
            start=datetime.now(),
            end=datetime.now(),
        )

    def __repr__(self) -> str:
        return f"Today({self.start})"


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

    __slots__ = ["start", "end", "days_ago"]

    def __init__(self, days_ago: int) -> None:
        super().__init__(
            start=datetime.now() - timedelta(days=days_ago),
            end=datetime.now(),
        )
        self.days_ago = days_ago

    def __repr__(self) -> str:
        return f"DaysAgo(days_ago={self.days_ago}, start={self.start}, end={self.end})"


class LaterThan(DateRange):
    """Period of time after a specific date as range for filtering sitemap URLs."""

    __slots__ = ["start", "end", "date"]

    def __init__(self, date: datetime) -> None:
        super().__init__(
            start=date,
            end=datetime.now(),
        )
        self.date = date

    def __repr__(self) -> str:
        return f"LaterThan(date={self.date}, start={self.start}, end={self.end})"


class EarlierThan(DateRange):
    """Period of time before a specific date as range for filtering sitemap URLs."""

    __slots__ = ["start", "end", "date"]

    def __init__(self, date: datetime) -> None:
        super().__init__(
            start=datetime.min,
            end=date,
        )
        self.date = date

    def __repr__(self) -> str:
        return f"EarlierThan(date={self.date}, start={self.start}, end={self.end})"
