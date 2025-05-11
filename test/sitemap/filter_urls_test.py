import pytest
from _helper.sitemap import get_mock_sitemap_content

from index_now.sitemap import filter_urls, parse_sitemap_xml_and_get_urls

TEST_URLS = parse_sitemap_xml_and_get_urls(get_mock_sitemap_content())


@pytest.mark.parametrize("urls, contains, skip, take, expected", [
    (TEST_URLS, None, None, None, TEST_URLS),
    (TEST_URLS, None, 0, None, TEST_URLS),
])
def test_filter_urls(urls: list[str], contains: str | None, skip: int | None, take: int | None, expected: list[str]) -> None:
    result = filter_urls(urls, contains)
    assert result == expected
