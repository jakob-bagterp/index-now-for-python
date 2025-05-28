from _helper.sitemap import get_mock_sitemap_content

from index_now.sitemap.parse import (
    parse_sitemap_xml_and_get_urls, parse_sitemap_xml_and_get_urls_as_elements)


def test_parse_sitemap_xml_and_get_urls() -> None:
    sitemap_content = get_mock_sitemap_content()
    urls = parse_sitemap_xml_and_get_urls(sitemap_content)
    assert len(urls) == 9
    assert urls[0] == "https://example.com"
    assert urls[-1] == "https://example.com/section2/subpage2"


def test_parse_sitemap_xml_and_get_urls_as_elements() -> None:
    sitemap_content = get_mock_sitemap_content()
    urls = parse_sitemap_xml_and_get_urls_as_elements(sitemap_content)
    assert len(urls) == 9
    first_url = urls[0]
    assert first_url.loc == "https://example.com"
    assert first_url.lastmod == "2025-01-01"
    assert first_url.changefreq == "always"
    assert first_url.priority == 1.0
    second_url = urls[1]
    assert second_url.loc == "https://example.com/page1"
    assert second_url.lastmod == "2025-02-01"
    assert second_url.changefreq == "hourly"
    assert second_url.priority == 0.8
    last_url = urls[-1]
    assert last_url.loc == "https://example.com/section2/subpage2"
    assert last_url.lastmod == "2025-09-01"
    assert last_url.changefreq == "weekly"
    assert last_url.priority == 0.1
