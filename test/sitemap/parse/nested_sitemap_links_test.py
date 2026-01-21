from _helper.sitemap import get_mock_sitemap_content

from index_now.sitemap.parse import \
    parse_sitemap_xml_and_get_nested_sitemap_links


def test_parse_sitemap_xml_and_get_sitemap_links() -> None:
    sitemap_content = get_mock_sitemap_content()
    sitemap_links = parse_sitemap_xml_and_get_nested_sitemap_links(sitemap_content)
    assert len(sitemap_links) == 2
    assert sitemap_links[0] == "https://example.com/nested_sitemap1.xml"
    assert sitemap_links[1] == "https://example.com/nested_sitemap2.xml"
