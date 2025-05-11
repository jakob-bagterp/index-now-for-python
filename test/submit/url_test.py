import pytest
from _helper.endpoint import TEMPORARILY_SKIPPED_ENDPOINTS, is_endpoint_up
from _mock_data.website import TIMER_FOR_PYTHON
from colorist import Color

from index_now import SearchEngineEndpoint, submit_url_to_index_now


@pytest.mark.parametrize("endpoint", [
    endpoint for endpoint in SearchEngineEndpoint
])
def test_submit_url_to_various_search_engines(endpoint: SearchEngineEndpoint, capfd: object) -> None:
    if endpoint in TEMPORARILY_SKIPPED_ENDPOINTS:
        pytest.skip(f"Endpoint is temporarily skipped: {endpoint}")
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")
    submit_url_to_index_now(TIMER_FOR_PYTHON.authentication, "https://jakob-bagterp.github.io/timer-for-python/", endpoint=endpoint)
    terminal_output, _ = capfd.readouterr()
    assert f"{Color.GREEN}URL submitted successfully to the IndexNow API:{Color.OFF} {endpoint}" in terminal_output
    assert f"Status code: {Color.GREEN}200{Color.OFF}" or f"Status code: {Color.GREEN}202{Color.OFF}" in terminal_output
