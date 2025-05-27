from dataclasses import dataclass
from datetime import datetime
from enum import Enum, unique


@unique
class ChangeFrequency(Enum):
    """The change frequency of a sitemap URL, e.g. `<changefreq>monthly</changefreq>`, and is used to indicate to a crawler how often the resource is expected to change. Reference: https://www.sitemaps.org/protocol.html#xmlTagDefinitions"""

    ALWYAS = "always"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    NEVER = "never"


@dataclass(slots=True, frozen=True)
class SitemapFilter:
    """Configuration class for filtering sitemap URLs based text, change frequency, date, and more.

    Attributes:
        change_frequency (ChangeFrequency | None): Optional filter for URLs based on change frequency. Ignored by default or if set to `None`.
        contains (str | None): Optional filter for URLs. Can be simple string (e.g. `"section1"`) or regular expression (e.g. `r"(section1)|(section2)"`). Ignored by default or if set to `None`.
        excludes (str | None): Optional filter for URLs. Can be simple string (e.g. `"not-include-this"`) or regular expression (e.g. `r"(not-include-this)|(not-include-that)"`). Ignored by default or if set to `None`.
        day (datetime | None): Optional filter for URLs based on a specific date. Ignored by default or if set to `None`.
        days_ago (int | None): Optional filter for URLs based on a number of days ago. Ignored by default or if set to `None`.
        later_than (datetime | None): Optional filter for URLs based on a date range. Ignored by default or if set to `None`.
        earlier_than (datetime | None): Optional filter for URLs based on a date range. Ignored by default or if set to `None`.
        skip (int | None): Optional number of URLs to be skipped. Ignored by default or if set to `None`.
        take (int | None): Optional limit of URLs to be taken. Ignored by default or if set to `None`.
    """

    change_frequency: ChangeFrequency | None = None
    contains: str | None = None
    excludes: str | None = None
    day: datetime | None = None
    days_ago: int | None = None
    later_than: datetime | None = None
    earlier_than: datetime | None = None
    skip: int | None = None
    take: int | None = None
