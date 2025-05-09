import pytest

from index_now.sitemap import filter_urls

TEST_URLS = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
]


@pytest.mark.parametrize("urls, contains, skip, take, expected", [
    (TEST_URLS, None, None, None, TEST_URLS),
])
def test_filter_urls(urls: list[str], contains: str | None, skip: int | None, take: int | None, expected: list[str]):
    result = filter_urls(urls, contains)
    assert result == expected
