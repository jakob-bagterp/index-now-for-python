import logging
from collections.abc import Callable
from typing import Any

import pytest

from index_now.sitemap.parse import (
    parse_sitemap_xml_and_get_nested_sitemap_links,
    parse_sitemap_xml_and_get_urls,
    parse_sitemap_xml_and_get_urls_as_elements,
)


@pytest.mark.parametrize(
    "parser",
    [
        parse_sitemap_xml_and_get_urls,
        parse_sitemap_xml_and_get_urls_as_elements,
        parse_sitemap_xml_and_get_nested_sitemap_links,
    ],
)
def test_error_handling_of_parsing_invalid_sitemap(
    parser: Callable[[str | bytes | Any], list[str]], caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.WARNING):
        parser("invalid sitemap content")
    assert (
        "Invalid sitemap format. The XML could not be parsed. Please check the location of the sitemap." in caplog.text
    )
