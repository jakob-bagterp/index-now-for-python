import pytest
from _helper.endpoint import TEMPORARILY_SKIPPED_ENDPOINTS, is_endpoint_up
from _mock_data.website import INDEX_NOW_FOR_PYTHON, INDEX_NOW_FOR_PYTHON_INVALID_API_KEY
from colorist import Color

from index_now import SearchEngineEndpoint, submit_urls_to_index_now
from index_now.sitemap.get import get_sitemap_xml
from index_now.sitemap.parse import parse_sitemap_xml_and_get_urls

INDEX_NOW_FOR_PYTHON_SITEMAP_URLS = parse_sitemap_xml_and_get_urls(
    get_sitemap_xml(INDEX_NOW_FOR_PYTHON.sitemap_location)
)


@pytest.mark.parametrize("endpoint", [endpoint for endpoint in SearchEngineEndpoint])
def test_submit_urls_to_various_search_engines(endpoint: SearchEngineEndpoint, capfd: object) -> None:
    if endpoint in TEMPORARILY_SKIPPED_ENDPOINTS:
        pytest.skip(f"Endpoint is temporarily skipped: {endpoint}")
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    assert len(INDEX_NOW_FOR_PYTHON_SITEMAP_URLS) > 10
    status_code = submit_urls_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, INDEX_NOW_FOR_PYTHON_SITEMAP_URLS, endpoint=endpoint
    )
    assert status_code in [200, 202]
    terminal_output, _ = capfd.readouterr()
    assert f"URL(s) were submitted successfully to this IndexNow API endpoint:{Color.OFF} {endpoint}" in terminal_output
    assert (
        f"Status code: {Color.GREEN}200 OK{Color.OFF}"
        or f"Status code: {Color.GREEN}202 Accepted{Color.OFF}" in terminal_output
    )


def test_submit_urls_error_handling_of_invalid_api_key(capfd: object) -> None:
    endpoint = SearchEngineEndpoint.BING
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    status_code = submit_urls_to_index_now(
        INDEX_NOW_FOR_PYTHON_INVALID_API_KEY.authentication,
        ["https://jakob-bagterp.github.io/invalid-url/"],
        endpoint=endpoint,
    )
    assert str(status_code).startswith("4")
    terminal_output, _ = capfd.readouterr()
    assert (
        f"{Color.YELLOW}Failure. No URL(s) were submitted to this IndexNow API endpoint:{Color.OFF} {endpoint}"
        in terminal_output
    )
    assert f"Status code: {Color.RED}4" in terminal_output
