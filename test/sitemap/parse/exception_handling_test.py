from collections.abc import Callable
from typing import Any

import pytest
from colorist import Color

from index_now.sitemap.parse import (
    parse_sitemap_xml_and_get_nested_sitemap_links,
    parse_sitemap_xml_and_get_urls, parse_sitemap_xml_and_get_urls_as_elements)


@pytest.mark.parametrize("parser", [
    parse_sitemap_xml_and_get_urls,
    parse_sitemap_xml_and_get_urls_as_elements,
    parse_sitemap_xml_and_get_nested_sitemap_links,
])
def test_error_handling_of_parsing_invalid_sitemap(parser: Callable[[str | bytes | Any], list[str]], capfd: object) -> None:
    parser("invalid sitemap content")
    terminal_output, _ = capfd.readouterr()
    assert f"{Color.YELLOW}Invalid sitemap format. The XML could not be parsed. Please check the location of the sitemap.{Color.OFF}" in terminal_output
