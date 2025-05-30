import pytest
from _helper.endpoint import TEMPORARILY_SKIPPED_ENDPOINTS, is_endpoint_up
from _mock_data.website import (INDEX_NOW_FOR_PYTHON,
                                INDEX_NOW_FOR_PYTHON_INVALID_API_KEY)
from colorist import Color

from index_now import SearchEngineEndpoint, submit_url_to_index_now


@pytest.mark.parametrize("endpoint", [
    endpoint for endpoint in SearchEngineEndpoint
])
def test_submit_url_to_various_search_engines(endpoint: SearchEngineEndpoint, capfd: object) -> None:
    if endpoint in TEMPORARILY_SKIPPED_ENDPOINTS:
        pytest.skip(f"Endpoint is temporarily skipped: {endpoint}")
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    status_code = submit_url_to_index_now(INDEX_NOW_FOR_PYTHON.authentication, "https://jakob-bagterp.github.io/index-now-for-python/", endpoint=endpoint)
    assert status_code in [200, 202]
    terminal_output, _ = capfd.readouterr()
    assert f"{Color.GREEN}1 URL was submitted successfully to this IndexNow API endpoint:{Color.OFF} {endpoint}" in terminal_output
    assert f"Status code: {Color.GREEN}200{Color.OFF}" or f"Status code: {Color.GREEN}202{Color.OFF}" in terminal_output


def test_submit_url_error_handling_of_invalid_api_key(capfd: object) -> None:
    endpoint = SearchEngineEndpoint.BING
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    status_code = submit_url_to_index_now(INDEX_NOW_FOR_PYTHON_INVALID_API_KEY.authentication, "https://jakob-bagterp.github.io/invalid-url/", endpoint=endpoint)
    assert str(status_code).startswith("4")
    terminal_output, _ = capfd.readouterr()
    assert f"{Color.YELLOW}Failure. No URL was submitted to this IndexNow API endpoint:{Color.OFF} {endpoint}" in terminal_output
    assert f"Status code: {Color.RED}4" in terminal_output
