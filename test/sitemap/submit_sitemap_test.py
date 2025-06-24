import pytest
from _helper.endpoint import TEMPORARILY_SKIPPED_ENDPOINTS, is_endpoint_up
from _mock_data.website import (BROWSERIST, COLORIST_FOR_PYTHON,
                                INDEX_NOW_FOR_PYTHON, TIMER_FOR_PYTHON,
                                IndexNowWebsiteData)
from colorist import Color

from index_now import (SearchEngineEndpoint, SitemapFilter,
                       submit_sitemap_to_index_now)


@pytest.mark.parametrize("website_data", [
    TIMER_FOR_PYTHON,
    COLORIST_FOR_PYTHON,
    BROWSERIST,
    INDEX_NOW_FOR_PYTHON,
])
def test_submit_sitemap_to_index_now(website_data: IndexNowWebsiteData, capfd: object) -> None:
    endpoint = SearchEngineEndpoint.YANDEX
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    status_code = submit_sitemap_to_index_now(website_data.authentication, website_data.sitemap_location, endpoint=endpoint)
    assert status_code in [200, 202]
    terminal_output, _ = capfd.readouterr()
    assert f"URL(s) were submitted successfully to this IndexNow API endpoint:{Color.OFF} {endpoint}" in terminal_output
    assert f"Status code: {Color.GREEN}200 OK{Color.OFF}" or f"Status code: {Color.GREEN}202 Accepted{Color.OFF}" in terminal_output


@pytest.mark.parametrize("endpoint", [
    endpoint for endpoint in SearchEngineEndpoint
])
def test_submit_sitemap_to_various_search_engines(endpoint: SearchEngineEndpoint, capfd: object) -> None:
    if endpoint in TEMPORARILY_SKIPPED_ENDPOINTS:
        pytest.skip(f"Endpoint is temporarily skipped: {endpoint}")
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    status_code = submit_sitemap_to_index_now(INDEX_NOW_FOR_PYTHON.authentication, INDEX_NOW_FOR_PYTHON.sitemap_location, endpoint=endpoint)
    assert status_code in [200, 202]
    terminal_output, _ = capfd.readouterr()
    assert f"URL(s) were submitted successfully to this IndexNow API endpoint:{Color.OFF} {endpoint}" in terminal_output
    assert f"Status code: {Color.GREEN}200 OK{Color.OFF}" or f"Status code: {Color.GREEN}202 Accepted{Color.OFF}" in terminal_output


def test_submit_sitemap_error_handling_of_invalid_sitemap() -> None:
    endpoint = SearchEngineEndpoint.YANDEX
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    status_code = submit_sitemap_to_index_now(INDEX_NOW_FOR_PYTHON.authentication, "https://jakob-bagterp.github.io/index-now-for-python/invalid_sitemap.xml", endpoint=endpoint)
    assert status_code == 404


def test_submit_sitemap_error_handling_of_no_matches() -> None:
    endpoint = SearchEngineEndpoint.YANDEX
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    sitemap_filter = SitemapFilter(contains="no-matches-at-all")
    status_code = submit_sitemap_to_index_now(INDEX_NOW_FOR_PYTHON.authentication, INDEX_NOW_FOR_PYTHON.sitemap_location, filter=sitemap_filter, endpoint=endpoint)
    assert status_code == 204
