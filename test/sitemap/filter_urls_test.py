from datetime import datetime

import pytest
from _helper.sitemap import (get_mock_sitemap_content, get_mock_sitemap_inconsistent_content,
                             get_mock_sitemap_only_urls_content)
from colorist import Color

from index_now import (Between, ChangeFrequency, DateRange, DaysAgo, EarlierThan, EarlierThanAndIncluding, LaterThan,
                       LaterThanAndIncluding, SitemapFilter, Today, Yesterday)
from index_now.sitemap.filter.sitemap import SitemapUrl, filter_sitemap_urls
from index_now.sitemap.parse import parse_sitemap_xml_and_get_urls_as_elements

SITEMAP = parse_sitemap_xml_and_get_urls_as_elements(get_mock_sitemap_content())
SITEMAP_LOC = [url.loc for url in SITEMAP]

SITEMAP_WITH_ONLY_URLS = parse_sitemap_xml_and_get_urls_as_elements(get_mock_sitemap_only_urls_content())
SITEMAP_WITH_ONLY_URLS_LOC = [url.loc for url in SITEMAP_WITH_ONLY_URLS]

SITEMAP_INCONSISTENT = parse_sitemap_xml_and_get_urls_as_elements(get_mock_sitemap_inconsistent_content())
SITEMAP_INCONSISTENT_LOC = [url.loc for url in SITEMAP_WITH_ONLY_URLS]

NO_MATCHES_AT_ALL = "no-matches-at-all"

MATCHES_ALL_URLS = "example.com"


@pytest.mark.parametrize("sitemap_urls, filter, expected", [
    ([], SitemapFilter(), []),

    # Sitemap with all <lastmod>, <changefreq>, and <priority> elements:
    (SITEMAP, SitemapFilter(), SITEMAP_LOC),
    (SITEMAP, SitemapFilter(skip=0), SITEMAP_LOC),
    (SITEMAP, SitemapFilter(take=0), []),
    (SITEMAP, SitemapFilter(skip=1), SITEMAP_LOC[1:]),
    (SITEMAP, SitemapFilter(skip=len(SITEMAP)), []),
    (SITEMAP, SitemapFilter(skip=0, take=1), SITEMAP_LOC[0:1]),
    (SITEMAP, SitemapFilter(contains="page1"), [SITEMAP_LOC[i] for i in [1, 5, 7]]),
    (SITEMAP, SitemapFilter(contains="page1", take=1), [SITEMAP_LOC[1]]),
    (SITEMAP, SitemapFilter(contains=r"(page1)|(section1)"), [SITEMAP_LOC[i] for i in [1, 5, 6, 7]]),
    (SITEMAP, SitemapFilter(contains=r"(page1)|(section1)", skip=1, take=2), [SITEMAP_LOC[i] for i in [5, 6]]),
    (SITEMAP, SitemapFilter(contains=r"^((?!section1).)*$"), [SITEMAP_LOC[i] for i in [0, 1, 2, 3, 4, 7, 8]]),
    (SITEMAP, SitemapFilter(contains=NO_MATCHES_AT_ALL), []),
    (SITEMAP, SitemapFilter(excludes="page"), SITEMAP_LOC[0:1]),
    (SITEMAP, SitemapFilter(excludes="/page"), [SITEMAP_LOC[i] for i in [0, 5, 6, 7, 8]]),
    (SITEMAP, SitemapFilter(excludes=r"(page1)|(section?\d)"), [SITEMAP_LOC[i] for i in [0, 2, 3, 4]]),
    (SITEMAP, SitemapFilter(excludes="subpage"), [SITEMAP_LOC[i] for i in [0, 1, 2, 3, 4]]),
    (SITEMAP, SitemapFilter(change_frequency=ChangeFrequency.DAILY), [SITEMAP_LOC[i] for i in [2, 7]]),
    (SITEMAP, SitemapFilter(change_frequency="daily"), [SITEMAP_LOC[i] for i in [2, 7]]),
    (SITEMAP, SitemapFilter(date_range=DateRange(start=datetime(2025, 3, 15), end=datetime(2025, 3, 20))), SITEMAP_LOC[8:]),
    (SITEMAP, SitemapFilter(date_range=Between(datetime(2025, 1, 20), datetime(2025, 2, 20))), SITEMAP_LOC[3:5]),
    (SITEMAP, SitemapFilter(date_range=Today()), []),
    (SITEMAP, SitemapFilter(date_range=Yesterday()), []),
    (SITEMAP, SitemapFilter(date_range=DaysAgo(2)), []),
    (SITEMAP, SitemapFilter(date_range=DaysAgo((datetime.today() - datetime(2025, 3, 15)).days)), SITEMAP_LOC[8:]),
    (SITEMAP, SitemapFilter(date_range=LaterThan(datetime(2025, 3, 10))), SITEMAP_LOC[8:]),
    (SITEMAP, SitemapFilter(date_range=LaterThanAndIncluding(datetime(2025, 3, 10))), SITEMAP_LOC[7:]),
    (SITEMAP, SitemapFilter(date_range=EarlierThan(datetime(2025, 1, 20))), SITEMAP_LOC[0:2]),
    (SITEMAP, SitemapFilter(date_range=EarlierThanAndIncluding(datetime(2025, 1, 20))), SITEMAP_LOC[0:3]),

    # Sitemap with only URLs and no <lastmod>, <changefreq>, and <priority> elements:
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(), SITEMAP_WITH_ONLY_URLS_LOC),
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(skip=0), SITEMAP_WITH_ONLY_URLS_LOC),
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(take=0), []),
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(skip=1), SITEMAP_WITH_ONLY_URLS_LOC[1:]),
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(skip=len(SITEMAP_WITH_ONLY_URLS)), []),
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(skip=0, take=1), SITEMAP_WITH_ONLY_URLS_LOC[0:1]),
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(contains="page1"), [SITEMAP_WITH_ONLY_URLS_LOC[i] for i in [1, 5, 7]]),
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(contains="page1", take=1), [SITEMAP_WITH_ONLY_URLS_LOC[1]]),
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(contains=r"(page1)|(section1)"), [SITEMAP_WITH_ONLY_URLS_LOC[i] for i in [1, 5, 6, 7]]),
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(contains=r"(page1)|(section1)", skip=1, take=2), [SITEMAP_WITH_ONLY_URLS_LOC[i] for i in [5, 6]]),
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(contains=r"^((?!section1).)*$"), [SITEMAP_WITH_ONLY_URLS_LOC[i] for i in [0, 1, 2, 3, 4, 7, 8]]),
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(contains=NO_MATCHES_AT_ALL), []),
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(excludes="page"), SITEMAP_WITH_ONLY_URLS_LOC[0:1]),
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(excludes="/page"), [SITEMAP_WITH_ONLY_URLS_LOC[i] for i in [0, 5, 6, 7, 8]]),
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(excludes=r"(page1)|(section?\d)"), [SITEMAP_WITH_ONLY_URLS_LOC[i] for i in [0, 2, 3, 4]]),
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(excludes="subpage"), [SITEMAP_WITH_ONLY_URLS_LOC[i] for i in [0, 1, 2, 3, 4]]),
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(change_frequency=ChangeFrequency.DAILY), SITEMAP_WITH_ONLY_URLS_LOC),  # Bypassed due to no <changefreq> element.
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(change_frequency="daily"), SITEMAP_WITH_ONLY_URLS_LOC),  # Bypassed due to no <changefreq> element.
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(date_range=DateRange(start=datetime(2025, 3, 15), end=datetime(2025, 3, 20))), SITEMAP_WITH_ONLY_URLS_LOC),  # Bypassed due to no <lastmod> element.
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(date_range=Between(datetime(2025, 1, 20), datetime(2025, 2, 20))), SITEMAP_WITH_ONLY_URLS_LOC),  # Bypassed due to no <lastmod> element.
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(date_range=Today()), SITEMAP_WITH_ONLY_URLS_LOC),  # Bypassed due to no <lastmod> element.
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(date_range=Yesterday()), SITEMAP_WITH_ONLY_URLS_LOC),  # Bypassed due to no <lastmod> element.
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(date_range=DaysAgo(2)), SITEMAP_WITH_ONLY_URLS_LOC),  # Bypassed due to no <lastmod> element.
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(date_range=DaysAgo((datetime.today() - datetime(2025, 3, 15)).days)), SITEMAP_WITH_ONLY_URLS_LOC),  # Bypassed due to no <lastmod> element.
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(date_range=LaterThan(datetime(2025, 3, 10))), SITEMAP_WITH_ONLY_URLS_LOC),  # Bypassed due to no <lastmod> element.
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(date_range=LaterThanAndIncluding(datetime(2025, 3, 10))), SITEMAP_WITH_ONLY_URLS_LOC),  # Bypassed due to no <lastmod> element.
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(date_range=EarlierThan(datetime(2025, 1, 20))), SITEMAP_WITH_ONLY_URLS_LOC),  # Bypassed due to no <lastmod> element.
    (SITEMAP_WITH_ONLY_URLS, SitemapFilter(date_range=EarlierThanAndIncluding(datetime(2025, 1, 20))), SITEMAP_WITH_ONLY_URLS_LOC),  # Bypassed due to no <lastmod> element.

    # Sitemap with inconsistent mix of <lastmod>, <changefreq>, and <priority> elements:
    (SITEMAP_INCONSISTENT, SitemapFilter(), SITEMAP_INCONSISTENT_LOC),
    (SITEMAP_INCONSISTENT, SitemapFilter(skip=0), SITEMAP_INCONSISTENT_LOC),
    (SITEMAP_INCONSISTENT, SitemapFilter(take=0), []),
    (SITEMAP_INCONSISTENT, SitemapFilter(skip=1), SITEMAP_INCONSISTENT_LOC[1:]),
    (SITEMAP_INCONSISTENT, SitemapFilter(skip=len(SITEMAP_INCONSISTENT)), []),
    (SITEMAP_INCONSISTENT, SitemapFilter(skip=0, take=1), SITEMAP_INCONSISTENT_LOC[0:1]),
    (SITEMAP_INCONSISTENT, SitemapFilter(contains="page1"), [SITEMAP_INCONSISTENT_LOC[i] for i in [1, 5, 7]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(contains="page1", take=1), [SITEMAP_INCONSISTENT_LOC[1]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(contains=r"(page1)|(section1)"), [SITEMAP_INCONSISTENT_LOC[i] for i in [1, 5, 6, 7]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(contains=r"(page1)|(section1)", skip=1, take=2), [SITEMAP_INCONSISTENT_LOC[i] for i in [5, 6]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(contains=r"^((?!section1).)*$"), [SITEMAP_INCONSISTENT_LOC[i] for i in [0, 1, 2, 3, 4, 7, 8]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(contains=NO_MATCHES_AT_ALL), []),
    (SITEMAP_INCONSISTENT, SitemapFilter(excludes="page"), SITEMAP_INCONSISTENT_LOC[0:1]),
    (SITEMAP_INCONSISTENT, SitemapFilter(excludes="/page"), [SITEMAP_INCONSISTENT_LOC[i] for i in [0, 5, 6, 7, 8]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(excludes=r"(page1)|(section?\d)"), [SITEMAP_INCONSISTENT_LOC[i] for i in [0, 2, 3, 4]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(excludes="subpage"), [SITEMAP_INCONSISTENT_LOC[i] for i in [0, 1, 2, 3, 4]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(change_frequency=ChangeFrequency.ALWAYS), [SITEMAP_INCONSISTENT_LOC[i] for i in [0, 1, 2, 4, 5, 7, 8]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(change_frequency="always"), [SITEMAP_INCONSISTENT_LOC[i] for i in [0, 1, 2, 4, 5, 7, 8]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(date_range=DateRange(start=datetime(2025, 3, 15), end=datetime(2025, 3, 20))), [SITEMAP_INCONSISTENT_LOC[i] for i in [1, 4, 5, 7, 8]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(date_range=Between(datetime(2025, 1, 20), datetime(2025, 2, 20))), [SITEMAP_INCONSISTENT_LOC[i] for i in [1, 3, 4, 5, 7]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(date_range=Today()), [SITEMAP_INCONSISTENT_LOC[i] for i in [1, 4, 5, 7]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(date_range=Yesterday()), [SITEMAP_INCONSISTENT_LOC[i] for i in [1, 4, 5, 7]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(date_range=DaysAgo(2)), [SITEMAP_INCONSISTENT_LOC[i] for i in [1, 4, 5, 7]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(date_range=DaysAgo((datetime.today() - datetime(2025, 3, 15)).days)), [SITEMAP_INCONSISTENT_LOC[i] for i in [1, 4, 5, 7, 8]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(date_range=LaterThan(datetime(2025, 3, 10))), [SITEMAP_INCONSISTENT_LOC[i] for i in [1, 4, 5, 7, 8]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(date_range=LaterThanAndIncluding(datetime(2025, 3, 10))), [SITEMAP_INCONSISTENT_LOC[i] for i in [1, 4, 5, 7, 8]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(date_range=EarlierThan(datetime(2025, 1, 20))), [SITEMAP_INCONSISTENT_LOC[i] for i in [0, 1, 4, 5, 7]]),
    (SITEMAP_INCONSISTENT, SitemapFilter(date_range=EarlierThanAndIncluding(datetime(2025, 1, 20))), [SITEMAP_INCONSISTENT_LOC[i] for i in [0, 1, 2, 4, 5, 7]]),
])
def test_filter_sitemap_urls(sitemap_urls: list[SitemapUrl], filter: SitemapFilter, expected: list[str]) -> None:
    filtered_urls = filter_sitemap_urls(sitemap_urls, filter)
    assert filtered_urls == expected


@pytest.mark.parametrize("sitemap_urls, filter, expected_terminal_output", [
    (SITEMAP, SitemapFilter(contains=NO_MATCHES_AT_ALL), f"{Color.YELLOW}No URLs contained the pattern \"{NO_MATCHES_AT_ALL}\".{Color.OFF}\n"),
    (SITEMAP, SitemapFilter(excludes=MATCHES_ALL_URLS), f"{Color.YELLOW}No URLs left after excluding the pattern \"{MATCHES_ALL_URLS}\".{Color.OFF}\n"),
    (SITEMAP, SitemapFilter(skip=100), f"{Color.YELLOW}No URLs left after skipping 100 URL(s) from sitemap.{Color.OFF}\n"),
    (SITEMAP, SitemapFilter(take=0), f"{Color.YELLOW}No URLs left. The value for take should be greater than 0.{Color.OFF}\n"),
])
def test_error_handling_of_filtering_sitemap_with_no_matches(sitemap_urls: list[SitemapUrl], filter: SitemapFilter, expected_terminal_output: str, capfd: object) -> None:
    filter_sitemap_urls(sitemap_urls, filter)
    terminal_output, _ = capfd.readouterr()
    assert expected_terminal_output in terminal_output
