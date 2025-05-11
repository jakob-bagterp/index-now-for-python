import pytest
from _helper.endpoint import TEMPORARILY_SKIPPED_ENDPOINTS, is_endpoint_up
from _mock_data.website import INDEX_NOW_FOR_PYTHON
from colorist import Color

from index_now import SearchEngineEndpoint, submit_urls_to_index_now
from index_now.sitemap import get_urls_from_sitemap_xml

INDEX_NOW_FOR_PYTHON_SITEMAP_URLS = get_urls_from_sitemap_xml(INDEX_NOW_FOR_PYTHON.sitemap_url)


@pytest.mark.parametrize("endpoint", [
    endpoint for endpoint in SearchEngineEndpoint
])
def test_submit_urls_to_various_search_engines(endpoint: SearchEngineEndpoint, capfd: object) -> None:
    if endpoint in TEMPORARILY_SKIPPED_ENDPOINTS:
        pytest.skip(f"Endpoint is temporarily skipped: {endpoint}")
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")
    assert len(INDEX_NOW_FOR_PYTHON_SITEMAP_URLS) > 10
    submit_urls_to_index_now(INDEX_NOW_FOR_PYTHON.authentication, INDEX_NOW_FOR_PYTHON_SITEMAP_URLS, endpoint=endpoint)
    terminal_output, _ = capfd.readouterr()
    assert f"URL(s) submitted successfully to the IndexNow API:{Color.OFF} {endpoint}" in terminal_output
    assert f"Status code: {Color.GREEN}200{Color.OFF}" or f"Status code: {Color.GREEN}202{Color.OFF}" in terminal_output
