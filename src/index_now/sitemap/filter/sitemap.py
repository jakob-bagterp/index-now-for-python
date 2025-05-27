from dataclasses import dataclass

from .change_frequency import ChangeFrequency
from .date_range import DateRange


@dataclass(slots=True, frozen=True)
class SitemapFilter:
    """Configuration class for filtering sitemap URLs based text, change frequency, date, and more.

    Attributes:
        change_frequency (ChangeFrequency | None): Optional filter for URLs based on change frequency. Ignored by default or if set to `None`.
        date_range (DateRange | None): Optional filter for URLs based on a date range, e.g. `Today`, `Day`, `DaysAgo`, `LaterThan`, `EarlierThan`, etc. Ignored by default or if set to `None`.
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
