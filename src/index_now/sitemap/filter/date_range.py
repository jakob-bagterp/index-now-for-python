from abc import ABC
from datetime import datetime, timedelta


class DateRange(ABC):
    """A date range for filtering sitemap URLs."""

    __slots__ = ["start", "end"]

    def __init__(self, start: datetime, end: datetime) -> None:
        self.start: datetime = start
        self.end: datetime = end

    def __repr__(self) -> str:
        return f"DateRange(start={self.start.date()}, end={self.end.date()})"

    def is_within_range(self, date: datetime) -> bool:
        """Check if a given date is within the date range."""

        return self.start.date() <= date.date() <= self.end.date()


class Today(DateRange):
    """Today as range for filtering sitemap URLs."""

    def __init__(self) -> None:
        super().__init__(
            start=datetime.today(),
            end=datetime.today(),
        )

    def __repr__(self) -> str:
        return f"Today({self.start.date()})"


class Day(DateRange):
    """A specific date for filtering sitemap URLs."""

    def __init__(self, day: datetime) -> None:
        super().__init__(
            start=day,
            end=day,
        )

    def __repr__(self) -> str:
        return f"Day(day={self.start.date()})"


class DaysAgo(DateRange):
    """A number of days ago from today as range for filtering sitemap URLs."""

    __slots__ = ["start", "end", "days_ago"]

    def __init__(self, days_ago: int) -> None:
        super().__init__(
            start=datetime.today() - timedelta(days=days_ago),
            end=datetime.today(),
        )
        self.days_ago = days_ago

    def __repr__(self) -> str:
        return f"DaysAgo(days_ago={self.days_ago}, start={self.start.date()}, end={self.end.date()})"


class LaterThan(DateRange):
    """Period of time after a specific date as range for filtering sitemap URLs."""

    __slots__ = ["start", "end", "date"]

    def __init__(self, date: datetime) -> None:
        super().__init__(
            start=date,
            end=datetime.max,
        )
        self.date = date

    def __repr__(self) -> str:
        return f"LaterThan(date={self.date.date()}, start={self.start.date()}, end={self.end.date()})"

    def is_within_range(self, date: datetime) -> bool:
        """Check if a given date is within the date range."""

        return self.start.date() < date.date()


class LaterThanAndIncluding(DateRange):
    """Period of time after and including a specific date as range for filtering sitemap URLs."""

    __slots__ = ["start", "end", "date"]

    def __init__(self, date: datetime) -> None:
        super().__init__(
            start=date,
            end=datetime.max,
        )
        self.date = date

    def __repr__(self) -> str:
        return f"LaterThan(date={self.date.date()}, start={self.start.date()}, end={self.end.date()})"

    def is_within_range(self, date: datetime) -> bool:
        """Check if a given date is within the date range."""

        return self.start.date() <= date.date()


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
        return f"EarlierThan(date={self.date.date()}, start={self.start.date()}, end={self.end.date()})"

    def is_within_range(self, date: datetime) -> bool:
        """Check if a given date is within the date range."""

        return date.date() < self.end.date()


class EarlierThanAndIncluding(DateRange):
    """Period of time before and including a specific date as range for filtering sitemap URLs."""

    __slots__ = ["start", "end", "date"]

    def __init__(self, date: datetime) -> None:
        super().__init__(
            start=datetime.min,
            end=date,
        )
        self.date = date

    def __repr__(self) -> str:
        return f"EarlierThan(date={self.date.date()}, start={self.start.date()}, end={self.end.date()})"

    def is_within_range(self, date: datetime) -> bool:
        """Check if a given date is within the date range."""

        return date.date() <= self.end.date()
