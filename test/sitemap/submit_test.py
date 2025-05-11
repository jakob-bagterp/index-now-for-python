import pytest
from _helper.endpoint import TEMPORARILY_SKIPPED_ENDPOINTS, is_endpoint_up
from _mock_data.website import (BROWSERIST, COLORIST_FOR_PYTHON,
                                INDEX_NOW_FOR_PYTHON, TIMER_FOR_PYTHON,
                                IndexNowWebsiteData)
from colorist import Color

from index_now import SearchEngineEndpoint, submit_sitemap_to_index_now


@pytest.mark.parametrize("website_data", [
    TIMER_FOR_PYTHON,
    COLORIST_FOR_PYTHON,
    BROWSERIST,
    INDEX_NOW_FOR_PYTHON,
])
def test_submit_sitemap_to_index_now(website_data: IndexNowWebsiteData, capfd: object) -> None:
    endpoint = SearchEngineEndpoint.INDEXNOW
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")
    submit_sitemap_to_index_now(website_data.authentication, website_data.sitemap_url, endpoint=endpoint)
    terminal_output, _ = capfd.readouterr()
    assert f"URL(s) submitted successfully to the IndexNow API:{Color.OFF} {endpoint}" in terminal_output
    assert f"Status code: {Color.GREEN}200{Color.OFF}" or f"Status code: {Color.GREEN}202{Color.OFF}" in terminal_output


@pytest.mark.parametrize("endpoint", [
    endpoint for endpoint in SearchEngineEndpoint
])
def test_submit_sitemap_to_various_search_engines(endpoint: SearchEngineEndpoint, capfd: object) -> None:
    if endpoint in TEMPORARILY_SKIPPED_ENDPOINTS:
        pytest.skip(f"Endpoint is temporarily skipped: {endpoint}")
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")
    submit_sitemap_to_index_now(INDEX_NOW_FOR_PYTHON.authentication, INDEX_NOW_FOR_PYTHON.sitemap_url, endpoint=endpoint)
    terminal_output, _ = capfd.readouterr()
    assert f"URL(s) submitted successfully to the IndexNow API:{Color.OFF} {endpoint}" in terminal_output
    assert f"Status code: {Color.GREEN}200{Color.OFF}" or f"Status code: {Color.GREEN}202{Color.OFF}" in terminal_output
