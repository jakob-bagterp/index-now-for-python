from colorist import Color

from ..authentication import IndexNowAuthentication
from ..endpoint import SearchEngineEndpoint
from ..url.submit import submit_urls_to_index_now
from .filter.sitemap import filter_urls, merge_and_remove_duplicates
from .get import get_urls_from_sitemap_xml


def submit_sitemap_to_index_now(authentication: IndexNowAuthentication, sitemap_location: str, contains: str | None = None, skip: int | None = None, take: int | None = None, endpoint: SearchEngineEndpoint | str = SearchEngineEndpoint.INDEXNOW) -> int:
    """Submit a sitemap to the IndexNow API of a search engine.

    Args:
        authentication (IndexNowAuthentication): Authentication credentials for the IndexNow API.
        sitemap_location (str): The URL of the sitemap to submit, e.g. `https://example.com/sitemap.xml`.
        contains (str | None): Optional filter for URLs. Can be simple string (e.g. `"section1"`) or regular expression (e.g. `r"(section1)|(section2)"`). Ignored by default or if set to `None`.
        skip (int | None): Optional number of URLs from the sitemap to be skipped. Ignored by default or if set to `None`.
        take (int | None): Optional limit of URLs from the sitemap to taken. Ignored by default and if set to  `None`.
        endpoint (SearchEngineEndpoint | str, optional): Select the search engine you want to submit to or use a custom URL as endpoint.

    Returns:
        int: Status code of the response, e.g. `200` or `202` for, respectively, success or accepted, or `400` for bad request, etc.

    Example:
        After adding your authentication credentials to the `IndexNowAuthentication` class, you can now submit an entire sitemap to the IndexNow API:

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

        If you want to only upload a portion of the sitemap URLs, alternatively use the `skip` and `take` parameters:

        ```python linenums="1" hl_lines="11-12"
        from index_now import submit_sitemap_to_index_now, IndexNowAuthentication

        authentication = IndexNowAuthentication(
            host="example.com",
            api_key="a1b2c3d4",
            api_key_location="https://example.com/a1b2c3d4.txt",
        )

        sitemap_location = "https://example.com/sitemap.xml"

        submit_sitemap_to_index_now(authentication, sitemap_location,
            skip=100, take=50)
        ```

        How to target URLs with a specific pattern by using the `contains` parameter:

        ```python linenums="11" hl_lines="1-2" title=""
        submit_sitemap_to_index_now(authentication, sitemap_location,
            contains="section1")
        ```

        The `contains` parameter also accepts regular expressions for more advanced filtering:

        ```python linenums="11" hl_lines="1-2" title=""
        submit_sitemap_to_index_now(authentication, sitemap_location,
            contains=r"(section1)|(section2)")
        ```

        Or combine the `contains`, `skip`, and `take` parameters to filter the URLs even further:

        ```python linenums="11" hl_lines="1-3" title=""
        submit_sitemap_to_index_now(authentication, sitemap_location,
            contains=r"(section1)|(section2)",
            skip=100, take=50)
        ```
    """

    urls = get_urls_from_sitemap_xml(sitemap_location)
    if not urls:
        raise ValueError(f"No URLs found in sitemap. Please check the sitemap location: {sitemap_location}")
    print(f"Found {Color.GREEN}{len(urls)} URL(s){Color.OFF} in total from sitemap.")

    if any([contains, skip, take]):
        urls = filter_urls(urls, contains, skip, take)
        if not urls:
            raise ValueError("No URLs left after filtering. Please check your filter parameters.")

    status_code = submit_urls_to_index_now(authentication, urls, endpoint)
    return status_code


def submit_sitemaps_to_index_now(authentication: IndexNowAuthentication, sitemap_locations: list[str], contains: str | None = None, skip: int | None = None, take: int | None = None, endpoint: SearchEngineEndpoint | str = SearchEngineEndpoint.INDEXNOW) -> int:
    """Submit multiple sitemaps to the IndexNow API of a search engine.

    Args:
        authentication (IndexNowAuthentication): Authentication credentials for the IndexNow API.
        sitemap_locations (list[str]): List of sitemap locations to submit, e.g. `["https://example.com/sitemap1.xml", "https://example.com/sitemap2.xml, "https://example.com/sitemap3.xml"]`.
        contains (str | None): Optional filter for URLs. Can be simple string (e.g. `"section1"`) or regular expression (e.g. `r"(section1)|(section2)"`). Ignored by default or if set to `None`.
        skip (int | None): Optional number of URLs from the sitemaps to be skipped. Ignored by default or if set to `None`.
        take (int | None): Optional limit of URLs from the sitemaps to be taken. Ignored by default or if set to `None`.
        endpoint (SearchEngineEndpoint | str, optional): Select the search engine you want to submit to or use a custom URL as endpoint.

    Returns:
        int: Status code of the response, e.g. `200` or `202` for, respectively, success or accepted, or `400` for bad request, etc.

    Example:
        After adding your authentication credentials to the `IndexNowAuthentication` class, you can now submit multiple sitemaps to the IndexNow API:

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

        If you want to only upload a portion of the sitemap URLs, alternatively use the `skip` and `take` parameters:

        ```python linenums="1" hl_lines="15-16"
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

        submit_sitemaps_to_index_now(authentication, sitemap_location,
            skip=100, take=50)
        ```

        How to target URLs with a specific pattern by using the `contains` parameter:

        ```python linenums="15" hl_lines="1-2" title=""
        submit_sitemaps_to_index_now(authentication, sitemap_location,
            contains="section1")
        ```

        The `contains` parameter also accepts regular expressions for more advanced filtering:

        ```python linenums="15" hl_lines="1-2" title=""
        submit_sitemaps_to_index_now(authentication, sitemap_location,
            contains=r"(section1)|(section2)")
        ```

        Or combine the `contains`, `skip`, and `take` parameters to filter the URLs even further:

        ```python linenums="15" hl_lines="1-3" title=""
        submit_sitemaps_to_index_now(authentication, sitemap_location,
            contains=r"(section1)|(section2)",
            skip=100, take=50)
        ```
    """

    urls: list[str] = []
    for sitemap_location in sitemap_locations:
        found_urls = get_urls_from_sitemap_xml(sitemap_location)
        urls = merge_and_remove_duplicates(urls, found_urls)
    if not urls:
        raise ValueError(f"No URLs found in sitemaps. Please check the sitemap locations: {sitemap_locations}")
    print(f"Found {Color.GREEN}{len(urls)} URL(s){Color.OFF} in total from sitemap.")

    if any([contains, skip, take]):
        urls = filter_urls(urls, contains, skip, take)
        if not urls:
            raise ValueError("No URLs left after filtering. Please check your filter parameters.")

    status_code = submit_urls_to_index_now(authentication, urls, endpoint)
    return status_code
