from collections.abc import Iterator
from http import HTTPStatus

import pytest
import requests
from _helper.flaky_server import FlakyEndpointServer, run_flaky_server
from _mock_data.website import INDEX_NOW_FOR_PYTHON
from colorist import Color
from urllib3.response import HTTPResponse

from index_now import http_client, submit_url_to_index_now, submit_urls_to_index_now


@pytest.fixture
def flaky_server(request: pytest.FixtureRequest) -> Iterator[FlakyEndpointServer]:
    with run_flaky_server(request.param) as server:
        yield server


@pytest.mark.parametrize(
    "flaky_server",
    [
        [None],
        [None, None, None],
        [HTTPStatus.SERVICE_UNAVAILABLE, None],
        [HTTPStatus.TOO_MANY_REQUESTS, HTTPStatus.BAD_GATEWAY],
    ],
    indirect=True,
)
def test_submit_urls_retries_until_success(
    flaky_server: FlakyEndpointServer, capfd: pytest.CaptureFixture[str]
) -> None:
    number_of_failures = len(flaky_server.failures)
    status_code = submit_urls_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication,
        ["https://jakob-bagterp.github.io/index-now-for-python/"],
        endpoint=flaky_server.endpoint,
    )
    assert status_code == HTTPStatus.OK
    assert flaky_server.request_count == number_of_failures + 1
    terminal_output, _ = capfd.readouterr()
    assert f"Status code: {Color.GREEN}200 OK{Color.OFF}" in terminal_output


@pytest.mark.parametrize("flaky_server", [[HTTPStatus.SERVICE_UNAVAILABLE, None]], indirect=True)
def test_submit_url_retries_until_success(flaky_server: FlakyEndpointServer) -> None:
    status_code = submit_url_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication,
        "https://jakob-bagterp.github.io/index-now-for-python/",
        endpoint=flaky_server.endpoint,
    )
    assert status_code == HTTPStatus.OK
    assert flaky_server.request_count == 3


@pytest.mark.parametrize("flaky_server", [[None] * (http_client.MAX_RETRIES + 1)], indirect=True)
def test_submit_urls_raises_when_retries_are_exhausted(flaky_server: FlakyEndpointServer) -> None:
    with pytest.raises(requests.exceptions.ConnectionError):
        submit_urls_to_index_now(
            INDEX_NOW_FOR_PYTHON.authentication,
            ["https://jakob-bagterp.github.io/index-now-for-python/"],
            endpoint=flaky_server.endpoint,
        )
    assert flaky_server.request_count == http_client.MAX_RETRIES + 1


@pytest.mark.parametrize(
    "flaky_server", [[HTTPStatus.SERVICE_UNAVAILABLE] * (http_client.MAX_RETRIES + 1)], indirect=True
)
def test_submit_urls_returns_last_status_code_when_retries_are_exhausted(
    flaky_server: FlakyEndpointServer, capfd: pytest.CaptureFixture[str]
) -> None:
    status_code = submit_urls_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication,
        ["https://jakob-bagterp.github.io/index-now-for-python/"],
        endpoint=flaky_server.endpoint,
    )
    assert status_code == HTTPStatus.SERVICE_UNAVAILABLE
    assert flaky_server.request_count == http_client.MAX_RETRIES + 1
    terminal_output, _ = capfd.readouterr()
    assert f"Status code: {Color.RED}503{Color.OFF}" in terminal_output


@pytest.mark.parametrize("flaky_server", [[HTTPStatus.BAD_REQUEST]], indirect=True)
def test_submit_urls_does_not_retry_client_errors(flaky_server: FlakyEndpointServer) -> None:
    status_code = submit_urls_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication,
        ["https://jakob-bagterp.github.io/index-now-for-python/"],
        endpoint=flaky_server.endpoint,
    )
    assert status_code == HTTPStatus.BAD_REQUEST
    assert flaky_server.request_count == 1


@pytest.mark.parametrize(
    "retry_after, expected_wait_in_seconds", [(None, None), ("3", 3), ("3600", http_client.MAX_RETRY_AFTER_IN_SECONDS)]
)
def test_retry_after_header_is_capped(retry_after: str | None, expected_wait_in_seconds: float | None) -> None:
    headers = {"Retry-After": retry_after} if retry_after is not None else {}
    response = HTTPResponse(headers=headers, status=HTTPStatus.TOO_MANY_REQUESTS)
    with http_client.create_session() as session:
        retry = session.get_adapter("https://").max_retries
    assert retry.get_retry_after(response) == expected_wait_in_seconds
