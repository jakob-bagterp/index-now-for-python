from _helper.sitemap import get_mock_sitemap_content

from index_now.sitemap.parse import \
    parse_sitemap_xml_and_get_nested_sitemap_links


def test_parse_sitemap_xml_and_get_urls() -> None:
    sitemap_content = get_mock_sitemap_content()
    links = parse_sitemap_xml_and_get_nested_sitemap_links(sitemap_content)
    assert len(links) == 2
    assert links[0] == "https://example.com/nested_sitemap1.xml"
    assert links[1] == "https://example.com/nested_sitemap2.xml"
