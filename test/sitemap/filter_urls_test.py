import pytest
from _helper.sitemap import get_mock_sitemap_content

from index_now.sitemap.filter.sitemap import filter_urls
from index_now.sitemap.parse import parse_sitemap_xml_and_get_urls

TEST_URLS = parse_sitemap_xml_and_get_urls(get_mock_sitemap_content())


@pytest.mark.parametrize("urls, contains, skip, take, expected", [
    (TEST_URLS, None, None, None, TEST_URLS),
    (TEST_URLS, None, 0, None, TEST_URLS),
    (TEST_URLS, None, None, 0, []),
    (TEST_URLS, None, 1, None, TEST_URLS[1:]),
    (TEST_URLS, None, len(TEST_URLS), None, []),
    (TEST_URLS, None, 0, 1, TEST_URLS[0:1]),
    (TEST_URLS, "page1", None, None, [TEST_URLS[i] for i in [1, 5, 7]]),
    (TEST_URLS, "page1", None, 1, [TEST_URLS[1]]),
    (TEST_URLS, r"(page1)|(section1)", None, None, [TEST_URLS[i] for i in [1, 5, 6, 7]]),
    (TEST_URLS, r"(page1)|(section1)", 1, 2, [TEST_URLS[i] for i in [5, 6]]),
    (TEST_URLS, "no-matches-at-all", None, None, []),
    ([], None, None, None, []),
])
def test_filter_urls(urls: list[str], contains: str | None, skip: int | None, take: int | None, expected: list[str]) -> None:
    filtered_urls = filter_urls(urls, contains, skip, take)
    assert filtered_urls == expected
