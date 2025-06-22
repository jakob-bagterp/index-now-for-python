from colorist import Color

from ..authentication import IndexNowAuthentication
from ..endpoint import SearchEngineEndpoint
from ..url.submit import submit_urls_to_index_now
from .filter.sitemap import SitemapFilter, filter_sitemap_urls
from .get import get_sitemap_xml
from .parse import (parse_sitemap_xml_and_get_urls,
                    parse_sitemap_xml_and_get_urls_as_elements)

UNPROCESSABLE_CONTENT_STATUS_CODE = 422


def submit_sitemap_to_index_now(authentication: IndexNowAuthentication, sitemap_location: str, filter: SitemapFilter | None = None, endpoint: SearchEngineEndpoint | str = SearchEngineEndpoint.INDEXNOW) -> int:
    """Submit a sitemap to the IndexNow API of a search engine.

    Args:
        authentication (IndexNowAuthentication): Authentication credentials for the IndexNow API.
        sitemap_location (str): The URL of the sitemap to submit, e.g. `https://example.com/sitemap.xml`.
        filter (SitemapFilter | None): Optional filter for URLs. Ignored by default or if set to `None`.
        endpoint (SearchEngineEndpoint | str, optional): Select the search engine you want to submit to or use a custom URL as endpoint.

    Returns:
        int: Status code of the response, e.g. `200` or `202` for, respectively, success or accepted, or `400` for bad request, etc.

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
    sitemap_xml = get_sitemap_xml(sitemap_location)
    if not filter:
        urls = parse_sitemap_xml_and_get_urls(sitemap_xml)
        if not urls:
            print(f"{Color.YELLOW}No URLs found in the sitemap. Please check the sitemap location: {sitemap_location}{Color.OFF}")
            return UNPROCESSABLE_CONTENT_STATUS_CODE
    else:
        url_elements = parse_sitemap_xml_and_get_urls_as_elements(sitemap_xml)
        urls = filter_sitemap_urls(url_elements, filter)
        if not urls:
            print(f"{Color.YELLOW}No URLs left after filtering. Please check your filter parameters.{Color.OFF}")
            return UNPROCESSABLE_CONTENT_STATUS_CODE
    if not urls:
        print(f"{Color.YELLOW}No URLs found in the sitemap. Please check the sitemap location: {sitemap_location}{Color.OFF}")
        return UNPROCESSABLE_CONTENT_STATUS_CODE
    else:
        print(f"Found {Color.GREEN}{len(urls):,} URL(s){Color.OFF} in total from this sitemap: {sitemap_location}")
        status_code = submit_urls_to_index_now(authentication, urls, endpoint)
        return status_code


def submit_sitemaps_to_index_now(authentication: IndexNowAuthentication, sitemap_locations: list[str], filter: SitemapFilter | None = None, endpoint: SearchEngineEndpoint | str = SearchEngineEndpoint.INDEXNOW) -> int:
    """Submit multiple sitemaps to the IndexNow API of a search engine.

    Args:
        authentication (IndexNowAuthentication): Authentication credentials for the IndexNow API.
        sitemap_locations (list[str]): List of sitemap locations to submit, e.g. `["https://example.com/sitemap1.xml", "https://example.com/sitemap2.xml, "https://example.com/sitemap3.xml"]`.
        filter (SitemapFilter | None): Optional filter for URLs. Ignored by default or if set to `None`.
        endpoint (SearchEngineEndpoint | str, optional): Select the search engine you want to submit to or use a custom URL as endpoint.

    Returns:
        int: Status code of the response, e.g. `200` or `202` for, respectively, success or accepted, or `400` for bad request, etc.

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
        submit_sitemaps_to_index_now(authentication, sitemap_location,
            endpoint="https://www.bing.com/indexnow")
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
    for sitemap_location in sitemap_locations:
        sitemap_xml = get_sitemap_xml(sitemap_location)
        if not filter:
            urls = parse_sitemap_xml_and_get_urls(sitemap_xml)
            merged_urls.extend(urls)
        else:
            url_elements = parse_sitemap_xml_and_get_urls_as_elements(sitemap_xml)
            merged_urls.extend(filter_sitemap_urls(url_elements, filter))
            if not merged_urls:
                print(f"{Color.YELLOW}No URLs left after filtering. Please check your filter parameters.{Color.OFF}")
                return UNPROCESSABLE_CONTENT_STATUS_CODE
    if not merged_urls:
        print(f"{Color.YELLOW}No URLs found in the sitemaps. Please check the sitemap locations: {', '.join(sitemap_locations)}{Color.OFF}")
        return UNPROCESSABLE_CONTENT_STATUS_CODE
    else:
        print(f"Found {Color.GREEN}{len(merged_urls):,} URL(s){Color.OFF} in total from these sitemaps: {', '.join(sitemap_locations)}")
        status_code = submit_urls_to_index_now(authentication, merged_urls, endpoint)
        return status_code
