import logging

import pytest
from _helper.endpoint import is_endpoint_up
from _helper.sitemap import INVALID_SITEMAP_LOCATIONS, NON_EXISTING_SITEMAP_LOCATIONS
from _mock_data.website import BROWSERIST, COLORIST_FOR_PYTHON, INDEX_NOW_FOR_PYTHON, TIMER_FOR_PYTHON

from index_now import SearchEngineEndpoint, SitemapFilter, submit_sitemaps_to_index_now

SITEMAP_LOCATIONS = [
    TIMER_FOR_PYTHON.sitemap_location,
    COLORIST_FOR_PYTHON.sitemap_location,
    BROWSERIST.sitemap_location,
    INDEX_NOW_FOR_PYTHON.sitemap_location,
]


def test_submit_multiple_sitemaps_to_index_now(caplog: pytest.LogCaptureFixture) -> None:
    endpoint = SearchEngineEndpoint.YANDEX
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    with caplog.at_level(logging.INFO):
        status_code = submit_sitemaps_to_index_now(
            INDEX_NOW_FOR_PYTHON.authentication, SITEMAP_LOCATIONS, endpoint=endpoint
        )
    assert status_code in [200, 202]
    assert f"URL(s) were submitted successfully to this IndexNow API endpoint: {endpoint}" in caplog.text
    assert "Status code: 200 OK" in caplog.text or "Status code: 202 Accepted" in caplog.text


def test_submit_multiple_sitemaps_error_handling_of_non_existing_sitemaps() -> None:
    endpoint = SearchEngineEndpoint.YANDEX
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    status_code = submit_sitemaps_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, NON_EXISTING_SITEMAP_LOCATIONS, endpoint=endpoint
    )
    assert status_code == 404


def test_submit_multiple_sitemaps_error_handling_of_no_matches() -> None:
    endpoint = SearchEngineEndpoint.YANDEX
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    sitemap_filter = SitemapFilter(contains="no-matches-at-all")
    status_code = submit_sitemaps_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, SITEMAP_LOCATIONS, filter=sitemap_filter, endpoint=endpoint
    )
    assert status_code == 204


def test_submit_multiple_sitemaps_error_handling_of_invalid_sitemaps() -> None:
    endpoint = SearchEngineEndpoint.YANDEX
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    status_code = submit_sitemaps_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, INVALID_SITEMAP_LOCATIONS, endpoint=endpoint
    )
    assert status_code == 422
