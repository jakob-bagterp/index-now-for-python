import pytest
from _mock_data.website import TIMER_FOR_PYTHON
from colorist import Color

from index_now import SearchEngineEndpoint, submit_url_to_index_now


def test_submit_url_to_index_now(capfd: object) -> None:
    submit_url_to_index_now(TIMER_FOR_PYTHON.authentication, "https://jakob-bagterp.github.io/timer-for-python/", endpoint=SearchEngineEndpoint.INDEXNOW)
    terminal_output, _ = capfd.readouterr()
    assert f"Status code: {Color.RED}422{Color.OFF}" in terminal_output


ENDPOINT_EXCEPTIONS = [
    SearchEngineEndpoint.YEP  # Fails with status code 400.
]


@pytest.mark.parametrize("endpoint", [
    endpoint for endpoint in SearchEngineEndpoint
])
def test_submit_url_to_various_search_engines(endpoint: SearchEngineEndpoint, capfd: object) -> None:
    submit_url_to_index_now(TIMER_FOR_PYTHON.authentication, "https://jakob-bagterp.github.io/timer-for-python/", endpoint=endpoint)
    terminal_output, _ = capfd.readouterr()
    if endpoint in ENDPOINT_EXCEPTIONS:
        pytest.skip(f"Endpoint {endpoint} gives different status code than expected.")
    assert f"Status code: {Color.RED}422{Color.OFF}" in terminal_output
