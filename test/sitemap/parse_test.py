from _helper.sitemap import get_mock_sitemap_content

from index_now.sitemap import parse_sitemap_xml_and_get_urls


def test_parse_sitemap_xml_and_get_urls() -> None:
    sitemap_content = get_mock_sitemap_content()
    urls = parse_sitemap_xml_and_get_urls(sitemap_content)
    assert len(urls) == 9
    assert urls[0] == "https://example.com"
    assert urls[-1] == "https://example.com/section2/subpage2"
