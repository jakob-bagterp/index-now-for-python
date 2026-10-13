from collections.abc import Iterator
from http import HTTPStatus

import pytest
from _helper.flaky_server import LOCALHOST, FlakyEndpointServer, run_flaky_server
from _helper.sitemap import get_mock_sitemap_content
from _mock_data.website import INDEX_NOW_FOR_PYTHON
from colorist import Color
from pytest import CaptureFixture, FixtureRequest, MonkeyPatch
from requests import Response
from requests.exceptions import ConnectionError
from urllib3.response import HTTPResponse

from index_now import (
    http_client,
    submit_sitemap_to_index_now,
    submit_sitemaps_to_index_now,
    submit_url_to_index_now,
    submit_urls_to_index_now,
)

RETRIES = 3

URLS = ["https://example.com"]


@pytest.fixture
def flaky_server(request: FixtureRequest) -> Iterator[FlakyEndpointServer]:
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
def test_submit_urls_retries_until_success(flaky_server: FlakyEndpointServer, capfd: CaptureFixture[str]) -> None:
    number_of_failures = len(flaky_server.failures)
    status_code = submit_urls_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, URLS, endpoint=flaky_server.endpoint, retries=RETRIES
    )
    assert status_code == HTTPStatus.OK
    assert flaky_server.request_count == number_of_failures + 1
    terminal_output, _ = capfd.readouterr()
    assert f"Status code: {Color.GREEN}200 OK{Color.OFF}" in terminal_output


@pytest.mark.parametrize("flaky_server", [[HTTPStatus.SERVICE_UNAVAILABLE, None]], indirect=True)
def test_submit_url_retries_until_success(flaky_server: FlakyEndpointServer) -> None:
    status_code = submit_url_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, URLS[0], endpoint=flaky_server.endpoint, retries=RETRIES
    )
    assert status_code == HTTPStatus.OK
    assert flaky_server.request_count == 3


@pytest.mark.parametrize("flaky_server", [[None] * (RETRIES + 1)], indirect=True)
def test_submit_urls_raises_when_retries_are_exhausted(flaky_server: FlakyEndpointServer) -> None:
    with pytest.raises(ConnectionError):
        submit_urls_to_index_now(
            INDEX_NOW_FOR_PYTHON.authentication, URLS, endpoint=flaky_server.endpoint, retries=RETRIES
        )
    assert flaky_server.request_count == RETRIES + 1


@pytest.mark.parametrize("flaky_server", [[HTTPStatus.SERVICE_UNAVAILABLE] * (RETRIES + 1)], indirect=True)
def test_submit_urls_returns_last_status_code_when_retries_are_exhausted(
    flaky_server: FlakyEndpointServer, capfd: CaptureFixture[str]
) -> None:
    status_code = submit_urls_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, URLS, endpoint=flaky_server.endpoint, retries=RETRIES
    )
    assert status_code == HTTPStatus.SERVICE_UNAVAILABLE
    assert flaky_server.request_count == RETRIES + 1
    terminal_output, _ = capfd.readouterr()
    assert f"Status code: {Color.RED}503{Color.OFF}" in terminal_output


@pytest.mark.parametrize("flaky_server", [[HTTPStatus.BAD_REQUEST]], indirect=True)
def test_submit_urls_does_not_retry_client_errors(flaky_server: FlakyEndpointServer) -> None:
    status_code = submit_urls_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, URLS, endpoint=flaky_server.endpoint, retries=RETRIES
    )
    assert status_code == HTTPStatus.BAD_REQUEST
    assert flaky_server.request_count == 1


@pytest.mark.parametrize("flaky_server", [[HTTPStatus.SERVICE_UNAVAILABLE]], indirect=True)
def test_submit_urls_does_not_retry_by_default(flaky_server: FlakyEndpointServer) -> None:
    status_code = submit_urls_to_index_now(INDEX_NOW_FOR_PYTHON.authentication, URLS, endpoint=flaky_server.endpoint)
    assert status_code == HTTPStatus.SERVICE_UNAVAILABLE
    assert flaky_server.request_count == 1


@pytest.mark.parametrize("flaky_server", [[None]], indirect=True)
def test_submit_url_does_not_retry_dropped_connection_by_default(flaky_server: FlakyEndpointServer) -> None:
    with pytest.raises(ConnectionError):
        submit_url_to_index_now(INDEX_NOW_FOR_PYTHON.authentication, URLS[0], endpoint=flaky_server.endpoint)
    assert flaky_server.request_count == 1


def test_negative_retries_raises_value_error() -> None:
    with pytest.raises(ValueError):
        submit_urls_to_index_now(INDEX_NOW_FOR_PYTHON.authentication, URLS, endpoint=f"http://{LOCALHOST}", retries=-1)


@pytest.mark.parametrize(
    "submit_sitemap, sitemap_argument",
    [
        (submit_sitemap_to_index_now, "https://example.com/sitemap.xml"),
        (submit_sitemaps_to_index_now, ["https://example.com/sitemap.xml"]),
    ],
)
def test_submit_sitemap_passes_retries_on(
    submit_sitemap: object, sitemap_argument: object, monkeypatch: MonkeyPatch
) -> None:
    retries_of_sitemap_requests: list[int] = []
    retries_of_submission: list[int] = []

    def fake_get(url: str, retries: int = 0, **kwargs: object) -> Response:
        retries_of_sitemap_requests.append(retries)
        response = Response()
        response.status_code = HTTPStatus.OK
        response._content = get_mock_sitemap_content().encode()
        return response

    def fake_submit_urls(*args: object, retries: int = 0, **kwargs: object) -> int:
        retries_of_submission.append(retries)
        return HTTPStatus.OK

    monkeypatch.setattr("index_now.http_client.get", fake_get)
    monkeypatch.setattr("index_now.sitemap.submit.submit_urls_to_index_now", fake_submit_urls)
    status_code = submit_sitemap(INDEX_NOW_FOR_PYTHON.authentication, sitemap_argument, retries=RETRIES)  # type: ignore[operator]
    assert status_code == HTTPStatus.OK
    assert retries_of_sitemap_requests == [RETRIES] * 3
    assert retries_of_submission == [RETRIES]


@pytest.mark.parametrize(
    "retry_after, expected_wait_in_seconds", [(None, None), ("3", 3), ("3600", http_client.MAX_RETRY_AFTER_IN_SECONDS)]
)
def test_retry_after_header_is_capped(retry_after: str | None, expected_wait_in_seconds: float | None) -> None:
    headers = {"Retry-After": retry_after} if retry_after is not None else {}
    response = HTTPResponse(headers=headers, status=HTTPStatus.TOO_MANY_REQUESTS)
    retry = http_client.CappedRetry()
    assert retry.get_retry_after(response) == expected_wait_in_seconds
