from collections.abc import Iterator
from contextlib import ExitStack
from http import HTTPStatus

import pytest
import requests
from _helper.flaky_server import FlakyEndpointServer, run_flaky_server
from _mock_data.website import INDEX_NOW_FOR_PYTHON
from colorist import Color
from pytest import CaptureFixture, FixtureRequest
from requests.exceptions import ConnectionError

from index_now import submit_url_to_index_now, submit_urls_to_index_now
from index_now.utility.submit_fallback import submit_with_fallback

URLS = ["https://jakob-bagterp.github.io/index-now-for-python/"]

ACCEPTED: list[HTTPStatus | None] = []

FAILING_ATTEMPTS = 10  # Fail on every attempt, so the endpoint fails no matter how many times the request is sent.

DROPPED = [None] * FAILING_ATTEMPTS  # Every attempt is dropped, like the sustained outage of Yandex.

UNAVAILABLE = [HTTPStatus.SERVICE_UNAVAILABLE] * FAILING_ATTEMPTS

FORBIDDEN = [HTTPStatus.FORBIDDEN]

BAD_REQUEST = [HTTPStatus.BAD_REQUEST]


@pytest.fixture
def flaky_servers(request: FixtureRequest) -> Iterator[list[FlakyEndpointServer]]:
    with ExitStack() as stack:
        yield [stack.enter_context(run_flaky_server(failures)) for failures in request.param]


@pytest.mark.parametrize(
    "flaky_servers",
    [
        [DROPPED, ACCEPTED],
        [UNAVAILABLE, ACCEPTED],
        [FORBIDDEN, ACCEPTED],
        [[HTTPStatus.TOO_MANY_REQUESTS] * FAILING_ATTEMPTS, ACCEPTED],
        [DROPPED, FORBIDDEN, ACCEPTED],
    ],
    indirect=True,
)
def test_submit_urls_falls_back_to_next_endpoint(
    flaky_servers: list[FlakyEndpointServer], capfd: CaptureFixture[str]
) -> None:
    *failing_servers, accepting_server = flaky_servers
    status_code = submit_urls_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, URLS, endpoint=[server.endpoint for server in flaky_servers]
    )
    assert status_code == HTTPStatus.OK
    assert all(server.request_count > 0 for server in failing_servers)
    assert accepting_server.request_count == 1
    terminal_output, _ = capfd.readouterr()
    for next_server in flaky_servers[1:]:
        assert f"Falling back to the next IndexNow API endpoint: {next_server.endpoint}" in terminal_output
    assert (
        f"1 URL(s) were submitted successfully to this IndexNow API endpoint:{Color.OFF} {accepting_server.endpoint}"
        in terminal_output
    )
    assert f"Status code: {Color.GREEN}200 OK{Color.OFF}" in terminal_output


@pytest.mark.parametrize("flaky_servers", [[DROPPED, ACCEPTED]], indirect=True)
def test_submit_url_falls_back_to_next_endpoint(
    flaky_servers: list[FlakyEndpointServer], capfd: CaptureFixture[str]
) -> None:
    dropping_server, accepting_server = flaky_servers
    status_code = submit_url_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, URLS[0], endpoint=[dropping_server.endpoint, accepting_server.endpoint]
    )
    assert status_code == HTTPStatus.OK
    assert dropping_server.request_count > 0
    assert accepting_server.request_count == 1
    terminal_output, _ = capfd.readouterr()
    assert (
        f"{Color.YELLOW}Failure. Could not connect to this IndexNow API endpoint:{Color.OFF} {dropping_server.endpoint}"
        in terminal_output
    )
    assert (
        f"1 URL was submitted successfully to this IndexNow API endpoint:{Color.OFF} {accepting_server.endpoint}"
        in terminal_output
    )


@pytest.mark.parametrize("flaky_servers", [[ACCEPTED, ACCEPTED]], indirect=True)
def test_submit_urls_stops_at_first_success(flaky_servers: list[FlakyEndpointServer]) -> None:
    first_server, second_server = flaky_servers
    status_code = submit_urls_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, URLS, endpoint=[first_server.endpoint, second_server.endpoint]
    )
    assert status_code == HTTPStatus.OK
    assert first_server.request_count == 1
    assert second_server.request_count == 0


@pytest.mark.parametrize("flaky_servers", [[BAD_REQUEST, ACCEPTED]], indirect=True)
def test_submit_urls_does_not_fall_back_on_bad_request(
    flaky_servers: list[FlakyEndpointServer], capfd: CaptureFixture[str]
) -> None:
    rejecting_server, unused_server = flaky_servers
    status_code = submit_urls_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, URLS, endpoint=[rejecting_server.endpoint, unused_server.endpoint]
    )
    assert status_code == HTTPStatus.BAD_REQUEST
    assert rejecting_server.request_count == 1
    assert unused_server.request_count == 0
    terminal_output, _ = capfd.readouterr()
    assert "Falling back" not in terminal_output
    assert f"Status code: {Color.RED}400{Color.OFF}" in terminal_output


@pytest.mark.parametrize(
    "flaky_servers, expected_status_code",
    [
        ([UNAVAILABLE, FORBIDDEN], HTTPStatus.FORBIDDEN),
        ([FORBIDDEN, UNAVAILABLE], HTTPStatus.SERVICE_UNAVAILABLE),
        ([UNAVAILABLE, DROPPED], HTTPStatus.SERVICE_UNAVAILABLE),
    ],
    indirect=["flaky_servers"],
)
def test_submit_urls_returns_last_status_code_when_all_endpoints_fail(
    flaky_servers: list[FlakyEndpointServer], expected_status_code: HTTPStatus, capfd: CaptureFixture[str]
) -> None:
    status_code = submit_urls_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, URLS, endpoint=[server.endpoint for server in flaky_servers]
    )
    assert status_code == expected_status_code
    assert all(server.request_count > 0 for server in flaky_servers)
    terminal_output, _ = capfd.readouterr()
    assert (
        f"{Color.YELLOW}Failure. None of the 2 IndexNow API endpoints accepted the submission.{Color.OFF}"
        in terminal_output
    )


@pytest.mark.parametrize("flaky_servers", [[DROPPED, DROPPED]], indirect=True)
def test_submit_urls_raises_when_no_endpoint_responds(flaky_servers: list[FlakyEndpointServer]) -> None:
    with pytest.raises(ConnectionError):
        submit_urls_to_index_now(
            INDEX_NOW_FOR_PYTHON.authentication, URLS, endpoint=[server.endpoint for server in flaky_servers]
        )
    assert all(server.request_count > 0 for server in flaky_servers)


@pytest.mark.parametrize("flaky_servers", [[FORBIDDEN]], indirect=True)
def test_submit_urls_with_single_endpoint_in_list_does_not_fall_back(
    flaky_servers: list[FlakyEndpointServer], capfd: CaptureFixture[str]
) -> None:
    status_code = submit_urls_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, URLS, endpoint=[flaky_servers[0].endpoint]
    )
    assert status_code == HTTPStatus.FORBIDDEN
    terminal_output, _ = capfd.readouterr()
    assert "Falling back" not in terminal_output
    assert "None of the" not in terminal_output


def test_submit_with_fallback_requires_at_least_one_endpoint() -> None:
    with pytest.raises(ValueError):
        submit_with_fallback([], send=requests.get, success_message="", failure_message="")


@pytest.mark.parametrize("flaky_servers", [[FORBIDDEN, ACCEPTED]], indirect=True)
def test_submit_urls_falls_back_with_tuple_of_endpoints(flaky_servers: list[FlakyEndpointServer]) -> None:
    rejecting_server, accepting_server = flaky_servers
    status_code = submit_urls_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, URLS, endpoint=(rejecting_server.endpoint, accepting_server.endpoint)
    )
    assert status_code == HTTPStatus.OK
    assert rejecting_server.request_count == 1
    assert accepting_server.request_count == 1
