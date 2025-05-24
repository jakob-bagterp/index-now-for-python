import pytest
from _helper.endpoint import is_endpoint_up
from _mock_data.website import (BROWSERIST, COLORIST_FOR_PYTHON,
                                INDEX_NOW_FOR_PYTHON, TIMER_FOR_PYTHON)
from colorist import Color

from index_now import SearchEngineEndpoint, submit_sitemaps_to_index_now

SITEMAP_URLS = [
    TIMER_FOR_PYTHON.sitemap_url,
    COLORIST_FOR_PYTHON.sitemap_url,
    BROWSERIST.sitemap_url,
    INDEX_NOW_FOR_PYTHON.sitemap_url,
]


def test_submit_multiple_sitemaps_to_index_now(capfd: object) -> None:
    endpoint = SearchEngineEndpoint.YANDEX
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    submit_sitemaps_to_index_now(INDEX_NOW_FOR_PYTHON.authentication, SITEMAP_URLS, endpoint=endpoint)
    terminal_output, _ = capfd.readouterr()
    assert f"URL(s) submitted successfully to the IndexNow API:{Color.OFF} {endpoint}" in terminal_output
    assert f"Status code: {Color.GREEN}200{Color.OFF}" or f"Status code: {Color.GREEN}202{Color.OFF}" in terminal_output


def test_submit_multiple_sitemaps_error_handling_of_invalid_sitemap() -> None:
    endpoint = SearchEngineEndpoint.YANDEX
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    with pytest.raises(ValueError):
        submit_sitemaps_to_index_now(INDEX_NOW_FOR_PYTHON.authentication, "https://jakob-bagterp.github.io/index-now-for-python/invalid_sitemap.xml", endpoint=endpoint)


def test_submit_multiple_sitemaps_error_handling_of_no_matches() -> None:
    endpoint = SearchEngineEndpoint.YANDEX
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    with pytest.raises(ValueError):
        submit_sitemaps_to_index_now(INDEX_NOW_FOR_PYTHON.authentication, SITEMAP_URLS, contains="no-matches-at-all", endpoint=endpoint)
