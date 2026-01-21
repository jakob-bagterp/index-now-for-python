from _helper.sitemap import get_mock_sitemap_with_nested_sitemaps_content

from index_now.sitemap.parse import (controller_parse_sitemap_xml_and_get_urls,
                                     parse_sitemap_xml_and_get_urls)


def test_controller_parse_sitemap_xml_and_get_urls() -> None:
    sitemap_content = get_mock_sitemap_with_nested_sitemaps_content()
    urls = controller_parse_sitemap_xml_and_get_urls(sitemap_content, as_elements=False)
    assert len(urls) > 10
    assert urls[0] == "https://example.com/page1"
    assert urls[1] == "https://jakob-bagterp.github.io/"
    assert urls[2].startswith("https://jakob-bagterp.github.io/colorist")
    assert not any(url.endswith(".xml") for url in urls)

    # Ensure that the same sitemap only yields a single URL when just parsing it:
    urls = parse_sitemap_xml_and_get_urls(sitemap_content)
    assert len(urls) == 1
    assert urls[0] == "https://example.com/page1"
