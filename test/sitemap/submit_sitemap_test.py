import logging

import pytest
from _helper.endpoint import TEMPORARILY_SKIPPED_ENDPOINTS, is_endpoint_up
from _helper.sitemap import INVALID_SITEMAP_LOCATION, NON_EXISTING_SITEMAP_LOCATION
from _mock_data.website import (
    BROWSERIST,
    COLORIST_FOR_PYTHON,
    INDEX_NOW_FOR_PYTHON,
    TIMER_FOR_PYTHON,
    IndexNowWebsiteData,
)

from index_now import SearchEngineEndpoint, SitemapFilter, submit_sitemap_to_index_now


@pytest.mark.parametrize("website_data", [TIMER_FOR_PYTHON, COLORIST_FOR_PYTHON, BROWSERIST, INDEX_NOW_FOR_PYTHON])
def test_submit_sitemap_to_index_now(website_data: IndexNowWebsiteData, caplog: pytest.LogCaptureFixture) -> None:
    endpoint = SearchEngineEndpoint.YANDEX
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    with caplog.at_level(logging.INFO):
        status_code = submit_sitemap_to_index_now(
            website_data.authentication, website_data.sitemap_location, endpoint=endpoint
        )
    assert status_code in [200, 202]
    assert f"URL(s) were submitted successfully to this IndexNow API endpoint: {endpoint}" in caplog.text
    assert "Status code: 200 OK" in caplog.text or "Status code: 202 Accepted" in caplog.text


@pytest.mark.parametrize("endpoint", [endpoint for endpoint in SearchEngineEndpoint])
def test_submit_sitemap_to_various_search_engines(
    endpoint: SearchEngineEndpoint, caplog: pytest.LogCaptureFixture
) -> None:
    if endpoint in TEMPORARILY_SKIPPED_ENDPOINTS:
        pytest.skip(f"Endpoint is temporarily skipped: {endpoint}")
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    with caplog.at_level(logging.INFO):
        status_code = submit_sitemap_to_index_now(
            INDEX_NOW_FOR_PYTHON.authentication, INDEX_NOW_FOR_PYTHON.sitemap_location, endpoint=endpoint
        )
    assert status_code in [200, 202]
    assert f"URL(s) were submitted successfully to this IndexNow API endpoint: {endpoint}" in caplog.text
    assert "Status code: 200 OK" in caplog.text or "Status code: 202 Accepted" in caplog.text


def test_submit_sitemap_error_handling_of_non_existing_sitemap() -> None:
    endpoint = SearchEngineEndpoint.YANDEX
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    status_code = submit_sitemap_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, NON_EXISTING_SITEMAP_LOCATION, endpoint=endpoint
    )
    assert status_code == 404


def test_submit_sitemap_error_handling_of_no_matches() -> None:
    endpoint = SearchEngineEndpoint.YANDEX
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    sitemap_filter = SitemapFilter(contains="no-matches-at-all")
    status_code = submit_sitemap_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication,
        INDEX_NOW_FOR_PYTHON.sitemap_location,
        filter=sitemap_filter,
        endpoint=endpoint,
    )
    assert status_code == 204


@pytest.mark.parametrize("sitemap_filter", [None, SitemapFilter(contains="no-matches-at-all")])
def test_submit_sitemap_error_handling_of_invalid_sitemap(sitemap_filter: SitemapFilter) -> None:
    endpoint = SearchEngineEndpoint.YANDEX
    if not is_endpoint_up(endpoint):
        pytest.skip(f"Endpoint is not up: {endpoint}")  # pragma: no cover
    status_code = submit_sitemap_to_index_now(
        INDEX_NOW_FOR_PYTHON.authentication, INVALID_SITEMAP_LOCATION, filter=sitemap_filter, endpoint=endpoint
    )
    assert status_code == 422
