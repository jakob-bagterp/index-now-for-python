from abc import ABC
from datetime import datetime, timedelta


class DateRange(ABC):
    """A date range for filtering sitemap URLs.

    Args:
        start (datetime): The start date of the range.
        end (datetime): The end date of the range.

    Example:
        ```python linenums="1" hl_lines="4-7"
        from datetime import datetime
        from index_now import DateRange, SitemapFilter

        date_range = DateRange(
            start=datetime(2025, 1, 1),
            end=datetime(2025, 1, 31),
        )

        filter = SitemapFilter(date_range=date_range)
        ```
    """

    __slots__ = ["start", "end"]

    def __init__(self, start: datetime, end: datetime) -> None:
        self.start: datetime = start
        self.end: datetime = end

    def __repr__(self) -> str:
        return f"DateRange(start={self.start.date()}, end={self.end.date()})"

    def is_within_range(self, date: datetime) -> bool:
        """Check if a given date is within the date range."""

        return self.start.date() <= date.date() <= self.end.date()


class Between(DateRange):
    """A date range between two not included dates for filtering sitemap URLs.

    Args:
        start (datetime): The start date of the range (not included in evaluation).
        end (datetime): The end date of the range (not included in evaluation).

    Example:
        ```python linenums="1" hl_lines="4-7"
        from datetime import datetime
        from index_now import Between, SitemapFilter

        date_range = Between(
            start=datetime(2025, 1, 1),
            end=datetime(2025, 1, 31),
        )

        filter = SitemapFilter(date_range=date_range)
        ```
    """

    __slots__ = ["start", "end"]

    def __init__(self, start: datetime, end: datetime) -> None:
        self.start: datetime = start
        self.end: datetime = end

    def __repr__(self) -> str:
        return f"Between(start={self.start.date()}, end={self.end.date()})"

    def is_within_range(self, date: datetime) -> bool:
        """Check if a given date is within the date range."""

        return self.start.date() < date.date() < self.end.date()


class Today(DateRange):
    """Today as range for filtering sitemap URLs.

    Example:
        ```python linenums="1" hl_lines="3"
        from index_now import Today, SitemapFilter

        filter = SitemapFilter(date_range=Today())
        ```
    """

    def __init__(self) -> None:
        super().__init__(
            start=datetime.today(),
            end=datetime.today(),
        )

    def __repr__(self) -> str:
        return f"Today({self.start.date()})"


class Yesterday(DateRange):
    """Yesterday as range for filtering sitemap URLs.

    Example:
        ```python linenums="1" hl_lines="3"
        from index_now import Yesterday, SitemapFilter

        filter = SitemapFilter(date_range=Yesterday())
        ```
    """

    def __init__(self) -> None:
        super().__init__(
            start=datetime.today() - timedelta(days=1),
            end=datetime.today() - timedelta(days=1),
        )

    def __repr__(self) -> str:
        return f"Yesterday({self.start.date()})"


class Day(DateRange):
    """A specific date for filtering sitemap URLs.

    Args:
        day (datetime): The specific day to filter sitemap URLs.

    Example:
        ```python linenums="1" hl_lines="4"
        from datetime import datetime
        from index_now import Day, SitemapFilter

        day = Day(datetime(2025, 1, 1))

        filter = SitemapFilter(date_range=day)
        ```
    """

    def __init__(self, day: datetime) -> None:
        super().__init__(
            start=day,
            end=day,
        )

    def __repr__(self) -> str:
        return f"Day(day={self.start.date()})"


class DaysAgo(DateRange):
    """A number of days ago from today as range for filtering sitemap URLs.

    Args:
        days_ago (int): The number of days ago to filter sitemap URLs.

    Example:
        ```python linenums="1" hl_lines="3"
        from index_now import DaysAgo, SitemapFilter

        days_ago = DaysAgo(2)

        filter = SitemapFilter(date_range=days_ago)
        ```
    """

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
    """Period of time after a specific date as range for filtering sitemap URLs.

    Args:
        date (datetime): The specific date to filter sitemap URLs.

    Example:
        ```python linenums="1" hl_lines="4"
        from datetime import datetime
        from index_now import LaterThan, SitemapFilter

        later_than = LaterThan(datetime(2025, 1, 1))

        filter = SitemapFilter(date_range=later_than)
        ```
    """

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
    """Period of time after and including a specific date as range for filtering sitemap URLs.

    Args:
        date (datetime): The specific date to filter sitemap URLs.

    Example:
        ```python linenums="1" hl_lines="4"
        from datetime import datetime
        from index_now import LaterThanAndIncluding, SitemapFilter

        later_than_including = LaterThanAndIncluding(datetime(2025, 1, 1))

        filter = SitemapFilter(date_range=later_than_including)
        ```
    """

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
    """Period of time before a specific date as range for filtering sitemap URLs.

    Args:
        date (datetime): The specific date to filter sitemap URLs.

    Example:
        ```python linenums="1" hl_lines="4"
        from datetime import datetime
        from index_now import EarlierThan, SitemapFilter

        earlier_than = EarlierThan(datetime(2025, 1, 1))

        filter = SitemapFilter(date_range=earlier_than)
        ```
    """

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
    """Period of time before and including a specific date as range for filtering sitemap URLs.

    Args:
        date (datetime): The specific date to filter sitemap URLs.

    Example:
        ```python linenums="1" hl_lines="4"
        from datetime import datetime
        from index_now import EarlierThanAndIncluding, SitemapFilter

        earlier_than_including = EarlierThanAndIncluding(datetime(2025, 1, 1))

        filter = SitemapFilter(date_range=earlier_than_including)
        ```
    """

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
