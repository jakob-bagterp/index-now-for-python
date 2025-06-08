import re
from dataclasses import dataclass
from datetime import datetime

from colorist import Color

from ..parse import SitemapUrl
from .change_frequency import ChangeFrequency
from .date_range import DateRange


@dataclass(slots=True, frozen=True)
class SitemapFilter:
    """Configuration class for filtering sitemap URLs based on text, change frequency, date ranges and other criteria.

    Attributes:
        change_frequency (ChangeFrequency | str | None): Optional filter for URLs based on change frequency, e.g. `daily`, `weekly`, `monthly`, etc. Note that if no `<changefreq>` element is found in the sitemap entry, the filter is bypassed. Ignored by default or if set to `None`.
        date_range (DateRange | None): Optional filter for URLs based on a date range, e.g. `Today`, `Day`, `DaysAgo`, `LaterThan`, `EarlierThan`, etc. Note that if no `<lastmod>` element is found in the sitemap entry, the filter is bypassed. Ignored by default or if set to `None`.
        contains (str | None): Optional filter for URLs. Can be simple string (e.g. `"section1"`) or regular expression (e.g. `r"(section1)|(section2)"`). Ignored by default or if set to `None`.
        excludes (str | None): Optional filter for URLs. Can be simple string (e.g. `"not-include-this"`) or regular expression (e.g. `r"(not-include-this)|(not-include-that)"`). Ignored by default or if set to `None`.
        skip (int | None): Optional number of URLs to be skipped. Ignored by default or if set to `None`.
        take (int | None): Optional limit of URLs to be taken. Ignored by default or if set to `None`.

    Example:
        Get all URLs containing `section1`:

        ```python linenums="1"
        from index_now import SitemapFilter

        filter = SitemapFilter(contains="section1")
        ```

        Get all URLs that contain either `section1` or `section2`:

        ```python linenums="1"
        from index_now import SitemapFilter

        filter = SitemapFilter(contains=r"(section1)|(section2)")
        ```

        Exclude any URL that contains `section3`:

        ```python linenums="1"
        from index_now import SitemapFilter

        filter = SitemapFilter(excludes="section3")
        ```

        Only the URLs modified within the past 2 days:

        ```python linenums="1"
        from index_now import SitemapFilter, DaysAgo

        filter = SitemapFilter(date_range=DaysAgo(2))
        ```

        Get all URLs from January, 2025:

        ```python linenums="1"
        from datetime import datetime
        from index_now import SitemapFilter, DateRange

        january_2025 = DateRange(
            start=datetime(2025, 1, 1),
            end=datetime(2025, 1, 31),
        )

        filter = SitemapFilter(date_range=january_2025)
        ```

        Get all URLs with a change frequency set to `daily`:

        ```python linenums="1"
        from index_now import SitemapFilter, ChangeFrequency

        filter = SitemapFilter(change_frequency=ChangeFrequency.DAILY)
        ```

        From a large sitemap, skip the first 10 URLs and take the next 20 URLs:

        ```python linenums="1"
        from index_now import SitemapFilter

        filter = SitemapFilter(skip=10, take=20)
        ```
    """

    change_frequency: ChangeFrequency | str | None = None
    date_range: DateRange | None = None
    contains: str | None = None
    excludes: str | None = None
    skip: int | None = None
    take: int | None = None


def filter_sitemap_urls(urls: list[SitemapUrl], filter: SitemapFilter) -> list[str]:
    """Filter URLs based on the given criteria.

    Args:
        urls (list[SitemapUrl]): List of URLs to be filtered.
        filter (SitemapFilter): Filter for URLs.

    Returns:
        list[str]: Filtered list of URLs, or empty list if no URLs are found.
    """

    def filter_by_change_frequency(urls: list[SitemapUrl], change_frequency: ChangeFrequency | str) -> list[SitemapUrl]:
        return [
            url for url in urls
            if not url.changefreq or url.changefreq.lower() == str(change_frequency).lower()
        ]

    def filter_by_date_range(urls: list[SitemapUrl], date_range: DateRange) -> list[SitemapUrl]:
        return [
            url for url in urls
            if not url.lastmod or date_range.is_within_range(datetime.fromisoformat(url.lastmod))
        ]

    if not urls:
        print(f"{Color.YELLOW}No URLs given before filtering.{Color.OFF}")
        return []

    if filter.change_frequency is not None:
        print(f"Number of URLs before filtering by change frequency {filter.change_frequency}: {len(urls)}")
        urls = filter_by_change_frequency(urls, filter.change_frequency)
        print(f"Number of URLs left after filtering by change frequency {filter.change_frequency}: {len(urls)}")

    if filter.date_range is not None:
        print(f"Number of URLs before filtering by date range {filter.date_range}: {len(urls)}")
        urls = filter_by_date_range(urls, filter.date_range)
        print(f"Number of URLs left after filtering by date range {filter.date_range}: {len(urls)}")

    if filter.contains is not None:
        print(f"Number of URLs before filtering by contains \"{filter.contains}\": {len(urls)}")
        pattern = re.compile(filter.contains)
        urls = [url for url in urls if pattern.search(url.loc)]
        if not urls:
            print(f"{Color.YELLOW}No URLs contained the pattern \"{filter.contains}\".{Color.OFF}")
            return []
        print(f"Number of URLs left after filtering by contains \"{filter.contains}\": {len(urls)}")

    if filter.excludes is not None:
        print(f"Number of URLs before filtering by excludes \"{filter.excludes}\": {len(urls)}")
        pattern = re.compile(filter.excludes)
        urls = [url for url in urls if not pattern.search(url.loc)]
        if not urls:
            print(f"{Color.YELLOW}No URLs left after excluding the pattern \"{filter.excludes}\".{Color.OFF}")
            return []
        print(f"Number of URLs left after filtering by excludes \"{filter.excludes}\": {len(urls)}")

    if filter.skip is not None:
        if filter.skip >= len(urls):
            print(f"{Color.YELLOW}No URLs left after skipping {filter.skip} URL(s) from sitemap.{Color.OFF}")
            return []
        print(f"Number of URLs before skipping {filter.skip} URL(s) from sitemap: {len(urls)}")
        urls = urls[filter.skip:]
        print(f"Number of URLs left after skipping {filter.skip} URL(s) from sitemap: {len(urls)}")

    if filter.take is not None:
        if filter.take <= 0:
            print(f"{Color.YELLOW}No URLs left. The value for take should be greater than 0.{Color.OFF}")
            return []
        print(f"Number of URLs before taking {filter.take} URL(s) from sitemap: {len(urls)}")
        urls = urls[:filter.take]
        print(f"Number of URLs left after taking {filter.take} URL(s) from sitemap: {len(urls)}")

    return [url.loc for url in urls]
