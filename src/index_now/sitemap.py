import re
from typing import Any

import lxml.etree
import requests
from colorist import Color

from .authentication import IndexNowAuthentication
from .endpoint import SearchEngineEndpoint
from .submit import submit_urls_to_index_now


def get_urls_from_sitemap_xml(sitemap_url: str) -> list[str]:
    """Get all URLs from a sitemap.xml file.

    Args:
        sitemap_url (str): The URL of the sitemap to get the URLs from.

    Returns:
        list[str] | None: List of URLs found in the sitemap.xml file, or empty list if no URLs are found.
    """

    response = requests.get(sitemap_url)
    return parse_sitemap_xml_and_get_urls(response.content)


def parse_sitemap_xml_and_get_urls(sitemap_content: str | bytes | Any) -> list[str]:
    """Parse the contents of a sitemap.xml file, e.g. from a response, and retrieve all the URLs from it.

    Args:
        content (str | bytes | Any): The content from the sitemap.xml file.

    Returns:
        list[str]: List of URLs found in the sitemap.xml file, or empty list if no URLs are found.
    """

    try:
        sitemap_tree = lxml.etree.fromstring(sitemap_content)
        urls = sitemap_tree.xpath("//ns:url/ns:loc/text()", namespaces={"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"})
        return [str(url).strip() for url in urls] if isinstance(urls, list) and urls else []
    except Exception:
        print(f"{Color.YELLOW}Invalid sitemap.xml format during parsing. Please check the sitemap URL.{Color.OFF}")
        return []


def filter_urls(urls: list[str], contains: str | None = None, skip: int | None = None, take: int | None = None) -> list[str]:
    """Filter URLs based on the given criteria.

    Args:
        urls (list[str]): List of URLs to be filtered.
        contains (str | None): Optional filter for URLs. Can be simple string (e.g. `"section1"`) or regular expression (e.g. `r"(section1)|(section2)"`). Ignored by default or if set to `None`.
        skip (int | None): Optional number of URLs to be skipped. Ignored by default or if set to `None`.
        take (int | None): Optional limit of URLs to be taken. Ignored by default and if set to  `None`.

    Returns:
        list[str]: Filtered list of URLs, or empty list if no URLs are found.
    """

    if not urls:
        print(f"{Color.YELLOW}No URLs given before filtering.{Color.OFF}")
        return []

    if contains is not None:
        pattern = re.compile(contains)
        urls = [url for url in urls if pattern.search(url)]
        if not urls:
            print(f"{Color.YELLOW}No URLs contained the pattern \"{contains}\".{Color.OFF}")
            return []

    if skip is not None:
        if skip >= len(urls):
            print(f"{Color.YELLOW}No URLs left after skipping {skip} URL(s) from sitemap.{Color.OFF}")
            return []
        urls = urls[skip:]

    if take is not None:
        if take <= 0:
            print(f"{Color.YELLOW}No URLs left. The value for take should be greater than 0.{Color.OFF}")
            return []
        urls = urls[:take]

    return urls


def submit_sitemap_to_index_now(authentication: IndexNowAuthentication, sitemap_url: str, contains: str | None = None, skip: int | None = None, take: int | None = None, endpoint: SearchEngineEndpoint | str = SearchEngineEndpoint.INDEXNOW) -> int:
    """Submit a sitemap to the IndexNow API of a search engine.

    Args:
        authentication (IndexNowAuthentication): Authentication credentials for the IndexNow API.
        sitemap_url (str): The URL of the sitemap to submit, e.g. `https://example.com/sitemap.xml`.
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

        sitemap_url = "https://example.com/sitemap.xml"

        submit_sitemap_to_index_now(authentication, sitemap_url)
        ```

        If you want to submit to a specific search engine, alternatively customize the endpoint:

        ```python linenums="11" hl_lines="1-2" title=""
        submit_sitemap_to_index_now(authentication, sitemap_url,
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

        sitemap_url = "https://example.com/sitemap.xml"

        submit_sitemap_to_index_now(authentication, sitemap_url,
            skip=100, take=50)
        ```

        How to target URLs with a specific pattern by using the `contains` parameter:

        ```python linenums="11" hl_lines="1-2" title=""
        submit_sitemap_to_index_now(authentication, sitemap_url,
            contains="section1")
        ```

        The `contains` parameter also accepts regular expressions for more advanced filtering:

        ```python linenums="11" hl_lines="1-2" title=""
        submit_sitemap_to_index_now(authentication, sitemap_url,
            contains=r"(section1)|(section2)")
        ```

        Or combine the `contains`, `skip`, and `take` parameters to filter the URLs even further:

        ```python linenums="11" hl_lines="1-3" title=""
        submit_sitemap_to_index_now(authentication, sitemap_url,
            contains=r"(section1)|(section2)",
            skip=100, take=50)
        ```
    """

    urls = get_urls_from_sitemap_xml(sitemap_url)
    if not urls:
        raise ValueError(f"No URLs found in sitemap. Please check the sitemap URL: {sitemap_url}")
    print(f"Found {Color.GREEN}{len(urls)} URL(s){Color.OFF} in total from sitemap.")

    if any([contains, skip, take]):
        urls = filter_urls(urls, contains, skip, take)
        if not urls:
            raise ValueError("No URLs left after filtering. Please check your filter parameters.")

    status_code = submit_urls_to_index_now(authentication, urls, endpoint)
    return status_code


def submit_sitemaps_to_index_now(authentication: IndexNowAuthentication, sitemap_urls: list[str], contains: str | None = None, skip: int | None = None, take: int | None = None, endpoint: SearchEngineEndpoint | str = SearchEngineEndpoint.INDEXNOW) -> int:
    """Submit multiple sitemaps to the IndexNow API of a search engine.

    Args:
        authentication (IndexNowAuthentication): Authentication credentials for the IndexNow API.
        sitemap_urls (list[str]): List of sitemap URLs to submit, e.g. `["https://example.com/sitemap1.xml", "https://example.com/sitemap2.xml, "https://example.com/sitemap3.xml"]`.
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

        sitemap_urls = [
            "https://example.com/sitemap1.xml",
            "https://example.com/sitemap2.xml",
            "https://example.com/sitemap3.xml",
        ]

        submit_sitemaps_to_index_now(authentication, sitemap_urls)
        ```

        If you want to submit to a specific search engine, alternatively customize the endpoint:

        ```python linenums="15" hl_lines="1-2" title=""
        submit_sitemaps_to_index_now(authentication, sitemap_url,
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

        sitemap_urls = [
            "https://example.com/sitemap1.xml",
            "https://example.com/sitemap2.xml",
            "https://example.com/sitemap3.xml",
        ]

        submit_sitemaps_to_index_now(authentication, sitemap_url,
            skip=100, take=50)
        ```

        How to target URLs with a specific pattern by using the `contains` parameter:

        ```python linenums="15" hl_lines="1-2" title=""
        submit_sitemaps_to_index_now(authentication, sitemap_url,
            contains="section1")
        ```

        The `contains` parameter also accepts regular expressions for more advanced filtering:

        ```python linenums="15" hl_lines="1-2" title=""
        submit_sitemaps_to_index_now(authentication, sitemap_url,
            contains=r"(section1)|(section2)")
        ```

        Or combine the `contains`, `skip`, and `take` parameters to filter the URLs even further:

        ```python linenums="15" hl_lines="1-3" title=""
        submit_sitemaps_to_index_now(authentication, sitemap_url,
            contains=r"(section1)|(section2)",
            skip=100, take=50)
        ```
    """

    urls: list[str] = []
    for sitemap_url in sitemap_urls:
        sitemap_urls_found = get_urls_from_sitemap_xml(sitemap_url)
        urls.extend([url for url in sitemap_urls_found if url not in urls])  # Ensure no duplicates.
    if not urls:
        raise ValueError(f"No URLs found in sitemaps. Please check the sitemap URLs: {sitemap_urls}")
    print(f"Found {Color.GREEN}{len(urls)} URL(s){Color.OFF} in total from sitemap.")

    if any([contains, skip, take]):
        urls = filter_urls(urls, contains, skip, take)
        if not urls:
            raise ValueError("No URLs left after filtering. Please check your filter parameters.")

    status_code = submit_urls_to_index_now(authentication, urls, endpoint)
    return status_code
