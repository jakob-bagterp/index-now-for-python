import lxml.etree
import requests
from colorist import Color

from .authentication import IndexNowAuthentication
from .submit import submit_urls_to_index_now


def get_urls_from_sitemap_xml(sitemap_url: str) -> list[str] | None:
    """Get all URLs from a sitemap.xml file.

    Args:
        sitemap_url (str): The URL of the sitemap to get the URLs from.

    Returns:
        list[str] | None: List of URLs found in the sitemap.xml file, or `None` if no URLs are found.
    """

    response = requests.get(sitemap_url)
    sitemap_tree = lxml.etree.fromstring(response.content)
    urls = sitemap_tree.xpath("//ns:url/ns:loc/text()", namespaces={"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"})
    return [str(url.strip()) for url in urls]


def filter_urls(urls: list[str], contains: str | None = None, skip: int | None = None, take: int | None = None) -> list[str]:
    """Filter URLs based on the given criteria.

    Args:
        urls (list[str]): List of URLs to be filtered.
        contains (str | None): Optional filter for URLs. If set, only URLs containing this string will be returned. Ignored by default and if set to `None`.
        skip (int | None): Optional number of URLs to be skipped. Ignored by default and if set to `None`.
        take (int | None): Optional limit of URLs to be taken. Ignored by default and if set to  `None`.

    Returns:
        list[str] | None: Filtered list of URLs, or `None` if no URLs are found.
    """

    if contains is not None:
        urls = [url for url in urls if contains in url]
        if not urls:
            raise ValueError(f"No URLs left after filtering URLs containing \"{contains}\".")

    if skip is not None:
        urls = urls[skip:]
        if not urls:
            raise ValueError(f"No URLs left after skipping {skip} URL(s) from sitemap.")

    if take is not None:
        urls = urls[:take]
        if not urls:
            raise ValueError(f"No URLs left after skipping {0 if skip is None else skip} and taking {take} URL(s) from sitemap.")

    return urls


def submit_sitemap_to_index_now(authentication: IndexNowAuthentication, sitemap_url: str, contains: str | None = None, skip: int | None = None, take: int | None = None) -> None:
    """Submit a sitemap to Bing's IndexNow API.

    Args:
        authentication (IndexNowAuthentication): Authentication data for the IndexNow API.
        sitemap_url (str): The URL of the sitemap to submit, e.g. `https://example.com/sitemap.xml`.
        contains (str | None): Optional filter for URLs in the sitemap. If set, only URLs containing this string will be submitted. Ignored by default and if set to `None`.
        skip (int | None): Optional number of URLs from the sitemap to be skipped. Ignored by default and if set to `None`.
        take (int | None): Optional limit of URLs from the sitemap to taken. Ignored by default and if set to  `None`.
    """

    urls = get_urls_from_sitemap_xml(sitemap_url)
    if not urls:
        raise ValueError(f"No URLs found in sitemap. Please check the sitemap URL: {sitemap_url}")
    print(f"Found {Color.GREEN}{len(urls)} URL(s){Color.OFF} in total from sitemap.")

    if any([contains, skip, take]):
        urls = filter_urls(urls, contains, skip, take)
        print(f"{Color.YELLOW}{len(urls)} URL(s) left after filtering.{Color.OFF}")

    submit_urls_to_index_now(authentication, urls)
