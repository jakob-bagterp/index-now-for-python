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

    sitemap_tree = lxml.etree.fromstring(sitemap_content)
    urls = sitemap_tree.xpath("//ns:url/ns:loc/text()", namespaces={"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"})
    return [str(url).strip() for url in urls] if isinstance(urls, list) and urls else []


def filter_urls(urls: list[str], contains: str | None = None, skip: int | None = None, take: int | None = None) -> list[str]:
    """Filter URLs based on the given criteria.

    Args:
        urls (list[str]): List of URLs to be filtered.
        contains (str | None): Optional filter for URLs. Can be simple string (e.g. `"section1"`) or regular expression (e.g. `r"(section1)|(section2)"`). Ignored by default and if set to `None`.
        skip (int | None): Optional number of URLs to be skipped. Ignored by default and if set to `None`.
        take (int | None): Optional limit of URLs to be taken. Ignored by default and if set to  `None`.

    Returns:
        list[str]: Filtered list of URLs, or empty list if no URLs are found.
    """

    def is_slice_out_of_range(slice: int, urls: list[str]) -> bool:
        return slice < 0 or slice >= len(urls)

    if not urls:
        print(f"{Color.YELLOW}No URLs left after filtering.{Color.OFF}")
        return []

    if contains is not None:
        pattern = re.compile(contains)
        urls = [url for url in urls if pattern.search(url)]
        if not urls:
            print(f"{Color.YELLOW}No URLs contained the pattern \"{contains}\".{Color.OFF}")
            return []

    if skip is not None:
        if is_slice_out_of_range(skip, urls):
            print(f"{Color.YELLOW}No URLs left after skipping {skip} URL(s) from sitemap.{Color.OFF}")
            return []
        urls = urls[skip:]

    if take is not None:
        if is_slice_out_of_range(take, urls):
            print(f"{Color.YELLOW}No URLs left after skipping {0 if skip is None else skip} and taking {take} URL(s) from sitemap.{Color.OFF}")
            return []
        urls = urls[:take]

    return urls


def submit_sitemap_to_index_now(authentication: IndexNowAuthentication, sitemap_url: str, contains: str | None = None, skip: int | None = None, take: int | None = None, endpoint: SearchEngineEndpoint | str = SearchEngineEndpoint.INDEXNOW) -> None:
    """Submit a sitemap to the IndexNow API of a search engine.

    Args:
        authentication (IndexNowAuthentication): Authentication data for the IndexNow API.
        sitemap_url (str): The URL of the sitemap to submit, e.g. `https://example.com/sitemap.xml`.
        contains (str | None): Optional filter for URLs in the sitemap. If set, only URLs containing this string will be submitted. Ignored by default and if set to `None`.
        skip (int | None): Optional number of URLs from the sitemap to be skipped. Ignored by default and if set to `None`.
        take (int | None): Optional limit of URLs from the sitemap to taken. Ignored by default and if set to  `None`.
        endpoint (SearchEngineEndpoint | str, optional): Select the search engine you want to submit to or use a custom URL as endpoint.
    """

    urls = get_urls_from_sitemap_xml(sitemap_url)
    if not urls:
        raise ValueError(f"No URLs found in sitemap. Please check the sitemap URL: {sitemap_url}")
    print(f"Found {Color.GREEN}{len(urls)} URL(s){Color.OFF} in total from sitemap.")

    if any([contains, skip, take]):
        urls = filter_urls(urls, contains, skip, take)
        if not urls:
            raise ValueError("No URLs left after filtering. Please check your filter parameters.")
        print(f"{Color.YELLOW}{len(urls)} URL(s) left after filtering.{Color.OFF}")

    submit_urls_to_index_now(authentication, urls, endpoint)
