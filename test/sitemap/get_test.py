from http import HTTPStatus

import pytest
import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException

from index_now.sitemap.get import get_sitemap_xml

SITEMAP_LOCATION = "https://example.com/sitemap.xml"


def test_get_sitemap_xml_raises_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    response = requests.Response()
    response.status_code = HTTPStatus.NOT_FOUND
    response.url = SITEMAP_LOCATION

    def fake_get(url: str, retries: int = 0, **kwargs: object) -> requests.Response:
        return response

    monkeypatch.setattr("index_now.sitemap.get.http_client.get", fake_get)

    with pytest.raises(HTTPError) as error:
        get_sitemap_xml(SITEMAP_LOCATION)

    assert error.value.response is response


def test_get_sitemap_xml_propagates_request_error_and_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    request_error = ConnectionError("Connection dropped")
    retries_used: list[int] = []

    def fake_get(url: str, retries: int = 0, **kwargs: object) -> requests.Response:
        retries_used.append(retries)
        raise request_error

    monkeypatch.setattr("index_now.sitemap.get.http_client.get", fake_get)

    with pytest.raises(RequestException) as error:
        get_sitemap_xml(SITEMAP_LOCATION, retries=3)

    assert error.value is request_error
    assert retries_used == [3]
