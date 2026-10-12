from collections.abc import Sequence
from http import HTTPStatus

import requests
from colorist import Color

from .. import http_client
from ..authentication import IndexNowAuthentication
from ..endpoint import SearchEngineEndpoint
from ..url.submit import submit_urls_to_index_now
from .filter.sitemap import SitemapFilter, filter_sitemap_urls
from .parse import SitemapUrl, controller_parse_sitemap_xml_and_get_urls


def submit_sitemap_to_index_now(
    authentication: IndexNowAuthentication,
    sitemap_location: str,
    filter: SitemapFilter | None = None,
    endpoint: SearchEngineEndpoint | str | Sequence[SearchEngineEndpoint | str] = SearchEngineEndpoint.INDEXNOW,
    retries: int = 0,
) -> int:
    """Submit a sitemap to the IndexNow API of a search engine. Note that nested sitemaps up to level 2 of the index sitemap will be included.

    Args:
        authentication (IndexNowAuthentication): Authentication credentials for the IndexNow API.
        sitemap_location (str): The URL of the sitemap to submit, e.g. `https://example.com/sitemap.xml`.
        filter (SitemapFilter | None): Optional filter for URLs. Ignored by default or if set to `None`.
        endpoint (SearchEngineEndpoint | str | Sequence[SearchEngineEndpoint | str], optional): Select the search engine you want to submit to or use a custom URL as endpoint. If a list or tuple of endpoints is given, they are tried in order until one accepts the submission. The submission falls back to the next endpoint on connection errors, server errors, `429 Too Many Requests` and `403 Forbidden`, but not on other client errors such as `400 Bad Request`.
        retries (int, optional): Number of times to retry a request on connection errors, timeouts, `429 Too Many Requests` and server errors, with exponential backoff. Defaults to `0`, i.e. no retries. If a list or tuple of endpoints is given, each endpoint is retried before falling back to the next one.

    Returns:
        int: Status code of the response, e.g. `200` or `202` for, respectively, success or accepted, or `400` for bad request, etc. If a list or tuple of endpoints is given and all of them fail, the last response status is returned if any endpoint responded; otherwise, the final connection error or timeout is raised.

    Example:
        After adding your authentication credentials to the [`IndexNowAuthentication`](../configuration/authentication.md) class, you can now submit an entire sitemap to the IndexNow API:

        ```python linenums="1" hl_lines="11"
        from index_now import submit_sitemap_to_index_now, IndexNowAuthentication

        authentication = IndexNowAuthentication(
            host="example.com",
            api_key="a1b2c3d4",
            api_key_location="https://example.com/a1b2c3d4.txt",
        )

        sitemap_location = "https://example.com/sitemap.xml"

        submit_sitemap_to_index_now(authentication, sitemap_location)
        ```

        If you want to submit to a specific search engine, alternatively customize the endpoint:

        ```python linenums="11" hl_lines="1-2" title=""
        submit_sitemap_to_index_now(authentication, sitemap_location,
            endpoint="https://www.bing.com/indexnow")
        ```

        Or provide a list of endpoints as fallback in case an endpoint is unavailable or rejects the submission. The endpoints are tried in order until one succeeds:

        ```python linenums="11" hl_lines="1-5 7" title=""
        endpoints_with_fallback = [
            "https://www.bing.com/indexnow",
            "https://yandex.com/indexnow",
            "https://search.seznam.cz/indexnow",
        ]

        submit_sitemap_to_index_now(authentication, sitemap_location, endpoint=endpoints_with_fallback)
        ```

        If you want to only upload a portion of the sitemap URLs, apply the `skip` and `take` parameters in the [`SitemapFilter`](../sitemap-filter/sitemap-filter.md) class:

        ```python linenums="1" hl_lines="11"
        from index_now import submit_sitemap_to_index_now, IndexNowAuthentication, SitemapFilter

        authentication = IndexNowAuthentication(
            host="example.com",
            api_key="a1b2c3d4",
            api_key_location="https://example.com/a1b2c3d4.txt",
        )

        sitemap_location = "https://example.com/sitemap.xml"

        filter = SitemapFilter(skip=100, take=50)

        submit_sitemap_to_index_now(authentication, sitemap_location, filter)
        ```

        Instead of filtering by amount, you can filter by last modified date using the `date_range` parameter. Firstly, add one of the [date range options](../sitemap-filter/date-range.md) to the imports, e.g. `DaysAgo`:

        ```python linenums="1" title=""
        from index_now import DaysAgo, submit_sitemaps_to_index_now, IndexNowAuthentication, SitemapFilter
        ```

        Then use the `date_range` parameter to filter URLs by last modified date:

        ```python linenums="11" hl_lines="1" title=""
        filter = SitemapFilter(date_range=DaysAgo(2))
        ```

        Or target URLs with a specific pattern using the `contains` parameter:

        ```python linenums="11" hl_lines="1" title=""
        filter = SitemapFilter(contains="section1")
        ```

        The `contains` parameter also accepts regular expressions for more advanced filtering:

        ```python linenums="11" hl_lines="1" title=""
        filter = SitemapFilter(contains=r"(section1)|(section2)")
        ```

        Or use the `excludes` parameter to exclude URLs that match a specific pattern:

        ```python linenums="11" hl_lines="1" title=""
        filter = SitemapFilter(excludes="page1")
        ```

        Or combine all the `contains` and `excludes`, `skip` and `take`, `date_range` and other parameters to filter the URLs even further:

        ```python linenums="11" hl_lines="1-8" title=""
        filter = SitemapFilter(
            date_range=DaysAgo(2),
            contains=r"(section1)|(section2)",
            excludes="page1",
            skip=100,
            take=50
        )
        ```
    """

    urls: list[str] = []
    response = http_client.get(sitemap_location, retries=retries)
    if response.status_code != HTTPStatus.OK:
        print(f"{Color.YELLOW}Failure. Please check the sitemap location: {sitemap_location}{Color.OFF}")
        print(f"Status code: {Color.RED}{response.status_code}{Color.OFF}")
        print(f"Response: {response.text}")
        return response.status_code

    if not filter:
        urls = controller_parse_sitemap_xml_and_get_urls(response.content, as_elements=False)
        if not urls:
            print(
                f"{Color.YELLOW}No URLs found in the sitemap. Please check the sitemap location: {sitemap_location}{Color.OFF}"
            )
            return HTTPStatus.UNPROCESSABLE_ENTITY
    else:
        url_elements = controller_parse_sitemap_xml_and_get_urls(response.content, as_elements=True)
        if not url_elements:
            print(
                f"{Color.YELLOW}No URLs found in the sitemap. Please check the sitemap location: {sitemap_location}{Color.OFF}"
            )
            return HTTPStatus.UNPROCESSABLE_ENTITY
        urls = filter_sitemap_urls(url_elements, filter)
        if not urls:
            print(f"{Color.YELLOW}No URLs left after filtering. Please check your filter parameters.{Color.OFF}")
            return HTTPStatus.NO_CONTENT

    print(f"Found {Color.GREEN}{len(urls):,} URL(s){Color.OFF} in total from this sitemap: {sitemap_location}")
    status_code = submit_urls_to_index_now(authentication, urls, endpoint=endpoint, retries=retries)
    return status_code


def submit_sitemaps_to_index_now(
    authentication: IndexNowAuthentication,
    sitemap_locations: list[str],
    filter: SitemapFilter | None = None,
    endpoint: SearchEngineEndpoint | str | Sequence[SearchEngineEndpoint | str] = SearchEngineEndpoint.INDEXNOW,
    retries: int = 0,
) -> int:
    """Submit multiple sitemaps to the IndexNow API of a search engine. Note that nested sitemaps up to level 2 of the index sitemaps will be included.

    Args:
        authentication (IndexNowAuthentication): Authentication credentials for the IndexNow API.
        sitemap_locations (list[str]): List of sitemap locations to submit, e.g. `["https://example.com/sitemap1.xml", "https://example.com/sitemap2.xml, "https://example.com/sitemap3.xml"]`.
        filter (SitemapFilter | None): Optional filter for URLs. Ignored by default or if set to `None`.
        endpoint (SearchEngineEndpoint | str | Sequence[SearchEngineEndpoint | str], optional): Select the search engine you want to submit to or use a custom URL as endpoint. If a list or tuple of endpoints is given, they are tried in order until one accepts the submission. The submission falls back to the next endpoint on connection errors, server errors, `429 Too Many Requests` and `403 Forbidden`, but not on other client errors such as `400 Bad Request`.
        retries (int, optional): Number of times to retry a request on connection errors, timeouts, `429 Too Many Requests` and server errors, with exponential backoff. Defaults to `0`, i.e. no retries. If a list or tuple of endpoints is given, each endpoint is retried before falling back to the next one.

    Returns:
        int: Status code of the response, e.g. `200` or `202` for, respectively, success or accepted, or `400` for bad request, etc. If a list or tuple of endpoints is given and all of them fail, the last response status is returned if any endpoint responded; otherwise, the final connection error or timeout is raised.

    Example:
        After adding your authentication credentials to the [`IndexNowAuthentication`](../configuration/authentication.md) class, you can now submit multiple sitemaps to the IndexNow API:

        ```python linenums="1" hl_lines="9-15"
        from index_now import submit_sitemaps_to_index_now, IndexNowAuthentication

        authentication = IndexNowAuthentication(
            host="example.com",
            api_key="a1b2c3d4",
            api_key_location="https://example.com/a1b2c3d4.txt",
        )

        sitemap_locations = [
            "https://example.com/sitemap1.xml",
            "https://example.com/sitemap2.xml",
            "https://example.com/sitemap3.xml",
        ]

        submit_sitemaps_to_index_now(authentication, sitemap_locations)
        ```

        If you want to submit to a specific search engine, alternatively customize the endpoint:

        ```python linenums="15" hl_lines="1-2" title=""
        submit_sitemaps_to_index_now(authentication, sitemap_locations,
            endpoint="https://www.bing.com/indexnow")
        ```

        Or provide a list of endpoints as fallback in case an endpoint is unavailable or rejects the submission. The endpoints are tried in order until one succeeds:

        ```python linenums="15" hl_lines="1-5 7" title=""
        endpoints_with_fallback = [
            "https://www.bing.com/indexnow",
            "https://yandex.com/indexnow",
            "https://search.seznam.cz/indexnow",
        ]

        submit_sitemaps_to_index_now(authentication, sitemap_locations, endpoint=endpoints_with_fallback)
        ```

        If you want to only upload a portion of the sitemap URLs, apply the `skip` and `take` parameters in the [`SitemapFilter`](../sitemap-filter/sitemap-filter.md) class:

        ```python linenums="1" hl_lines="15"
        from index_now import submit_sitemaps_to_index_now, IndexNowAuthentication, SitemapFilter

        authentication = IndexNowAuthentication(
            host="example.com",
            api_key="a1b2c3d4",
            api_key_location="https://example.com/a1b2c3d4.txt",
        )

        sitemap_locations = [
            "https://example.com/sitemap1.xml",
            "https://example.com/sitemap2.xml",
            "https://example.com/sitemap3.xml",
        ]

        filter = SitemapFilter(skip=100, take=50)

        submit_sitemaps_to_index_now(authentication, sitemap_location, filter)
        ```

        Instead of filtering by amount, you can filter by last modified date using the `date_range` parameter. Firstly, add one of the [date range options](../sitemap-filter/date-range.md) to the imports, e.g. `DaysAgo`:

        ```python linenums="1" title=""
        from index_now import DaysAgo, submit_sitemaps_to_index_now, IndexNowAuthentication, SitemapFilter
        ```

        Then use the `date_range` parameter to filter URLs by last modified date:

        ```python linenums="15" hl_lines="1" title=""
        filter = SitemapFilter(date_range=DaysAgo(2))
        ```

        Or target URLs with a specific pattern using the `contains` parameter:

        ```python linenums="15" hl_lines="1" title=""
        filter = SitemapFilter(contains="section1")
        ```

        The `contains` parameter also accepts regular expressions for more advanced filtering:

        ```python linenums="15" hl_lines="1" title=""
        filter = SitemapFilter(contains=r"(section1)|(section2)")
        ```

        Or use the `excludes` parameter to exclude URLs that match a specific pattern:

        ```python linenums="15" hl_lines="1" title=""
        filter = SitemapFilter(excludes="page1")
        ```

        Or combine all the `contains` and `excludes`, `skip` and `take`, `date_range` and other parameters to filter the URLs even further:

        ```python linenums="15" hl_lines="1-8" title=""
        filter = SitemapFilter(
            date_range=DaysAgo(2),
            contains=r"(section1)|(section2)",
            excludes="page1",
            skip=100,
            take=50
        )
        ```
    """

    merged_urls: list[str] = []
    responses: list[requests.Response] = []
    for sitemap_location in sitemap_locations:
        response = http_client.get(sitemap_location, retries=retries)
        if response.status_code != HTTPStatus.OK:
            print(f"{Color.YELLOW}Failure. Please check the sitemap location: {sitemap_location}{Color.OFF}")
            print(f"Status code: {Color.RED}{response.status_code}{Color.OFF}")
            print(f"Response: {response.text}")
            return response.status_code
        urls = controller_parse_sitemap_xml_and_get_urls(response.content, as_elements=False)
        if not urls:
            print(
                f"{Color.YELLOW}No URLs found in the sitemap. Please check the sitemap location: {sitemap_location}{Color.OFF}"
            )
            return HTTPStatus.UNPROCESSABLE_ENTITY
        merged_urls.extend(urls)
        responses.append(response)

    if filter:
        url_elements: list[SitemapUrl] = []
        for response in responses:
            url_elements.extend(controller_parse_sitemap_xml_and_get_urls(response.content, as_elements=True))
        merged_urls = filter_sitemap_urls(url_elements, filter)
        if not merged_urls:
            print(f"{Color.YELLOW}No URLs left after filtering. Please check your filter parameters.{Color.OFF}")
            return HTTPStatus.NO_CONTENT

    print(
        f"Found {Color.GREEN}{len(merged_urls):,} URL(s){Color.OFF} in total from these sitemaps: {', '.join(sitemap_locations)}"
    )
    status_code = submit_urls_to_index_now(authentication, merged_urls, endpoint=endpoint, retries=retries)
    return status_code
