import re
from dataclasses import dataclass

from colorist import Color

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


def filter_urls(urls: list[str], contains: str | None = None, skip: int | None = None, take: int | None = None) -> list[str]:
    """Filter URLs based on the given criteria.

    Args:
        urls (list[str]): List of URLs to be filtered.
        contains (str | None): Optional filter for URLs. Can be simple string (e.g. `"section1"`) or regular expression (e.g. `r"(section1)|(section2)"`). Ignored by default or if set to `None`.
        skip (int | None): Optional number of URLs to be skipped. Ignored by default or if set to `None`.
        take (int | None): Optional limit of URLs to be taken. Ignored by default and if set to  `None`.

    Returns:
        list[str]: Filtered list of URLs, or empty list if no URLs are found.
    """

    if not urls:
        print(f"{Color.YELLOW}No URLs given before filtering.{Color.OFF}")
        return []

    if contains is not None:
        pattern = re.compile(contains)
        urls = [url for url in urls if pattern.search(url)]
        if not urls:
            print(f"{Color.YELLOW}No URLs contained the pattern \"{contains}\".{Color.OFF}")
            return []

    if skip is not None:
        if skip >= len(urls):
            print(f"{Color.YELLOW}No URLs left after skipping {skip} URL(s) from sitemap.{Color.OFF}")
            return []
        urls = urls[skip:]

    if take is not None:
        if take <= 0:
            print(f"{Color.YELLOW}No URLs left. The value for take should be greater than 0.{Color.OFF}")
            return []
        urls = urls[:take]

    return urls


def merge_and_remove_duplicates(urls1: list[str], urls2: list[str]) -> list[str]:
    """Merge and remove duplicate URLs from two lists.

    Args:
        urls1 (list[str]): List of URLs to merge with.
        urls2 (list[str]): List of URLs to merge with.

    Returns:
        list[str]: List of URLs with duplicates removed.
    """

    return sorted(list(set(urls1) | set(urls2)))
