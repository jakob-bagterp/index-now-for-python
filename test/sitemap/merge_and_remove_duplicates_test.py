import pytest

from index_now.sitemap import merge_and_remove_duplicates

URLS_1 = ["https://example.com", "https://example.com/section1", "https://example.com/section1/page1", "https://example.com/section1/page2", "https://example.com/section2"]
URLS_2 = ["https://example.com", "https://example.com/section1", "https://example.com/section2", "https://example.com/section3"]
URLS_DUPLICATES = ["https://example.com", "https://example.com"]


@pytest.mark.parametrize("urls1, urls2, expected", [
    (URLS_1, [], URLS_1),
    ([], URLS_1, URLS_1),
    (URLS_2, [], URLS_2),
    ([], URLS_2, URLS_2),
    (URLS_1, URLS_2, ["https://example.com", "https://example.com/section1", "https://example.com/section1/page1", "https://example.com/section1/page2", "https://example.com/section2", "https://example.com/section3"]),
    (URLS_DUPLICATES, [], ["https://example.com"]),
    ([], URLS_DUPLICATES, ["https://example.com"]),
    ([], [], []),
])
def test_remove_duplicates(urls1: list[str], urls2: list[str], expected: list[str]) -> None:
    merged_urls = merge_and_remove_duplicates(urls1, urls2)
    assert len(merged_urls) == len(expected)
    assert merged_urls == expected
