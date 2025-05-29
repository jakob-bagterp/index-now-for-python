from datetime import datetime

import pytest
from _helper.sitemap import get_mock_sitemap_content

from index_now import (Between, ChangeFrequency, DateRange, DaysAgo,
                       EarlierThan, EarlierThanAndIncluding, LaterThan,
                       LaterThanAndIncluding, SitemapFilter, Today, Yesterday)
from index_now.sitemap.filter.sitemap import SitemapUrl, filter_sitemap_urls
from index_now.sitemap.parse import parse_sitemap_xml_and_get_urls_as_elements

SITEMAP_URLS = parse_sitemap_xml_and_get_urls_as_elements(get_mock_sitemap_content())
SITEMAP_URLS_LOC = [url.loc for url in SITEMAP_URLS]


@pytest.mark.parametrize("sitemap_urls, filter, expected", [
    (SITEMAP_URLS, SitemapFilter(), SITEMAP_URLS_LOC),
    (SITEMAP_URLS, SitemapFilter(skip=0), SITEMAP_URLS_LOC),
    (SITEMAP_URLS, SitemapFilter(take=0), []),
    (SITEMAP_URLS, SitemapFilter(skip=1), SITEMAP_URLS_LOC[1:]),
    (SITEMAP_URLS, SitemapFilter(skip=len(SITEMAP_URLS)), []),
    (SITEMAP_URLS, SitemapFilter(skip=0, take=1), SITEMAP_URLS_LOC[0:1]),
    (SITEMAP_URLS, SitemapFilter(contains="page1"), [SITEMAP_URLS_LOC[i] for i in [1, 5, 7]]),
    (SITEMAP_URLS, SitemapFilter(contains="page1", take=1), [SITEMAP_URLS_LOC[1]]),
    (SITEMAP_URLS, SitemapFilter(contains=r"(page1)|(section1)"), [SITEMAP_URLS_LOC[i] for i in [1, 5, 6, 7]]),
    (SITEMAP_URLS, SitemapFilter(contains=r"(page1)|(section1)", skip=1, take=2), [SITEMAP_URLS_LOC[i] for i in [5, 6]]),
    (SITEMAP_URLS, SitemapFilter(contains="no-matches-at-all"), []),
    (SITEMAP_URLS, SitemapFilter(excludes="page"), SITEMAP_URLS_LOC[0:1]),
    (SITEMAP_URLS, SitemapFilter(excludes="/page"), [SITEMAP_URLS_LOC[i] for i in [0, 5, 6, 7, 8]]),
    (SITEMAP_URLS, SitemapFilter(excludes=r"(page1)|(section?\d)"), [SITEMAP_URLS_LOC[i] for i in [0, 2, 3, 4]]),
    (SITEMAP_URLS, SitemapFilter(excludes="subpage"), [SITEMAP_URLS_LOC[i] for i in [0, 1, 2, 3, 4]]),
    (SITEMAP_URLS, SitemapFilter(change_frequency=ChangeFrequency.DAILY), [SITEMAP_URLS_LOC[i] for i in [2, 7]]),
    (SITEMAP_URLS, SitemapFilter(change_frequency="daily"), [SITEMAP_URLS_LOC[i] for i in [2, 7]]),
    (SITEMAP_URLS, SitemapFilter(date_range=DateRange(start=datetime(2025, 3, 15), end=datetime(2025, 3, 20))), SITEMAP_URLS_LOC[8:]),
    (SITEMAP_URLS, SitemapFilter(date_range=Between(datetime(2025, 1, 20), datetime(2025, 2, 20))), SITEMAP_URLS_LOC[3:5]),
    (SITEMAP_URLS, SitemapFilter(date_range=Today()), []),
    (SITEMAP_URLS, SitemapFilter(date_range=Yesterday()), []),
    (SITEMAP_URLS, SitemapFilter(date_range=DaysAgo(2)), []),
    (SITEMAP_URLS, SitemapFilter(date_range=DaysAgo((datetime.today() - datetime(2025, 3, 15)).days)), SITEMAP_URLS_LOC[8:]),
    (SITEMAP_URLS, SitemapFilter(date_range=LaterThan(datetime(2025, 3, 10))), SITEMAP_URLS_LOC[8:]),
    (SITEMAP_URLS, SitemapFilter(date_range=LaterThanAndIncluding(datetime(2025, 3, 10))), SITEMAP_URLS_LOC[7:]),
    (SITEMAP_URLS, SitemapFilter(date_range=EarlierThan(datetime(2025, 1, 20))), SITEMAP_URLS_LOC[0:2]),
    (SITEMAP_URLS, SitemapFilter(date_range=EarlierThanAndIncluding(datetime(2025, 1, 20))), SITEMAP_URLS_LOC[0:3]),
    ([], SitemapFilter(), []),
])
def test_filter_sitemap_urls(sitemap_urls: list[SitemapUrl], filter: SitemapFilter, expected: list[str]) -> None:
    filtered_urls = filter_sitemap_urls(sitemap_urls, filter)
    assert filtered_urls == expected
