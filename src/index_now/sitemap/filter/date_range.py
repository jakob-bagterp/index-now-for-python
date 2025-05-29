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

        january_2025 = DateRange(
            start=datetime(2025, 1, 1),
            end=datetime(2025, 1, 31),
        )

        filter = SitemapFilter(date_range=january_2025)
        ```
    """

    __slots__ = ["start", "end"]

    def __init__(self, start: datetime, end: datetime) -> None:
        self.start: datetime = start
        self.end: datetime = end

    def __repr__(self) -> str:
        return f"DateRange(start={self.start.date()}, end={self.end.date()})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return all([
            self.__slots__ == other.__slots__,
            self.__str__() == other.__str__(),
            self.start.date() == other.start.date(),
            self.end.date() == other.end.date(),
        ])

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

        january_2_to_30_2025 = Between(
            start=datetime(2025, 1, 1),
            end=datetime(2025, 1, 31),
        )

        filter = SitemapFilter(date_range=january_2_to_30_2025)
        ```
    """

    def __init__(self, start: datetime, end: datetime) -> None:
        super().__init__(
            start=start,
            end=end,
        )

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

        today = Today()

        filter = SitemapFilter(date_range=today)
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

        yesterday = Yesterday()

        filter = SitemapFilter(date_range=yesterday)
        ```
    """

    def __init__(self) -> None:
        super().__init__(
            start=datetime.today() - timedelta(days=1),
            end=datetime.today() - timedelta(days=1),
        )

    def __repr__(self) -> str:
        return f"Yesterday(start={self.start.date()}, end={self.end.date()})"


class Day(DateRange):
    """A specific date for filtering sitemap URLs.

    Args:
        day (datetime): The specific day to filter sitemap URLs.

    Example:
        ```python linenums="1" hl_lines="4"
        from datetime import datetime
        from index_now import Day, SitemapFilter

        new_year_2025 = Day(datetime(2025, 1, 1))

        filter = SitemapFilter(date_range=new_year_2025)
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

        two_days_ago = DaysAgo(2)

        filter = SitemapFilter(date_range=two_days_ago)
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

        after_new_year_2025 = LaterThan(datetime(2025, 1, 1))

        filter = SitemapFilter(date_range=after_new_year_2025)
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

        new_year_2025_or_later = LaterThanAndIncluding(datetime(2025, 1, 1))

        filter = SitemapFilter(date_range=new_year_2025_or_later)
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

        before_2025 = EarlierThan(datetime(2025, 1, 1))

        filter = SitemapFilter(date_range=before_2025)
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

        new_year_2025_or_before = EarlierThanAndIncluding(datetime(2025, 1, 1))

        filter = SitemapFilter(date_range=new_year_2025_or_before)
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
