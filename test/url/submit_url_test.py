import logging

import pytest
from _helper.endpoint import TEMPORARILY_SKIPPED_ENDPOINTS, is_endpoint_up
from _mock_data.website import INDEX_NOW_FOR_PYTHON, INDEX_NOW_FOR_PYTHON_INVALID_API_KEY

from index_now import SearchEngineEndpoint, submit_url_to_index_now


@pytest.mark.parametrize("endpoint", [endpoint for endpoint in SearchEngineEndpoint])
def test_submit_url_to_various_search_engines(endpoint: SearchEngineEndpoint, caplog: pytest.LogCaptureFixture) -> None:
    if endpoint in TEMPORARILY_SKIPPED_ENDPOINTS:
        pytest.skip(f"Endpoint is temporarily skipped: {endpoint}")
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    with caplog.at_level(logging.INFO):
        status_code = submit_url_to_index_now(
            INDEX_NOW_FOR_PYTHON.authentication,
            "https://jakob-bagterp.github.io/index-now-for-python/",
            endpoint=endpoint,
        )
    assert status_code in [200, 202]
    assert f"1 URL was submitted successfully to this IndexNow API endpoint: {endpoint}" in caplog.text
    assert "Status code: 200 OK" in caplog.text or "Status code: 202 Accepted" in caplog.text


def test_submit_url_error_handling_of_invalid_api_key(caplog: pytest.LogCaptureFixture) -> None:
    endpoint = SearchEngineEndpoint.BING
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    with caplog.at_level(logging.WARNING):
        status_code = submit_url_to_index_now(
            INDEX_NOW_FOR_PYTHON_INVALID_API_KEY.authentication,
            "https://jakob-bagterp.github.io/invalid-url/",
            endpoint=endpoint,
        )
    assert str(status_code).startswith("4")
    assert f"Failure. No URL was submitted to this IndexNow API endpoint: {endpoint}" in caplog.text
    assert "Status code: 4" in caplog.text
