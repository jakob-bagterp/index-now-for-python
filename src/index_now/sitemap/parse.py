from dataclasses import dataclass
from typing import Any

import lxml.etree
from colorist import Color

SITEMAP_SCHEMA_NAMESPACE = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}


@dataclass(slots=True, frozen=True)
class SitemapUrl:
    """Reprensents an `<url>...</url>` element in an XML sitemap file so it can be parsed in a data structure.

    Attributes:
        loc (str): The location of the URL.
        lastmod (str | None): The last modification date of the URL. Optional.
        changefreq (str | None): The change frequency of the URL. Optional.
        priority (float | None): The priority of the URL. Optional.
    """

    loc: str
    lastmod: str | None = None
    changefreq: str | None = None
    priority: float | None = None


def parse_sitemap_xml_and_get_urls_as_elements(sitemap_content: str | bytes | Any) -> list[SitemapUrl]:
    """Parse the contents of an XML sitemap file, e.g. from a response, and retrieve all the URLs from it as `SitemapUrl` elements.

    Args:
        content (str | bytes | Any): The content of the XML sitemap file.

    Returns:
        list[SitemapUrl]: List of SitemapUrl objects found in the XML sitemap file, or empty list if no URLs are found.
    """

    try:
        urls: list[SitemapUrl] = []
        sitemap_tree = lxml.etree.fromstring(sitemap_content)
        sitemap_urls = sitemap_tree.xpath("//ns:url", namespaces=SITEMAP_SCHEMA_NAMESPACE)
        for sitemap_url in sitemap_urls:  # type: ignore
            loc = sitemap_url.xpath("ns:loc/text()", namespaces=SITEMAP_SCHEMA_NAMESPACE)[0].strip()  # type: ignore
            lastmod = next(iter(sitemap_url.xpath("ns:lastmod/text()", namespaces=SITEMAP_SCHEMA_NAMESPACE)), None)  # type: ignore
            changefreq = next(iter(sitemap_url.xpath("ns:changefreq/text()", namespaces=SITEMAP_SCHEMA_NAMESPACE)), None)  # type: ignore
            priority = next(iter(sitemap_url.xpath("ns:priority/text()", namespaces=SITEMAP_SCHEMA_NAMESPACE)), None)  # type: ignore
            url = SitemapUrl(
                loc=str(loc),
                lastmod=str(lastmod) if lastmod else None,
                changefreq=str(changefreq) if changefreq else None,
                priority=float(priority) if priority is not None else None
            )
            urls.append(url)
        return urls
    except Exception:
        print(f"{Color.YELLOW}Invalid sitemap format. The XML could not be parsed. Please check the location of the sitemap.{Color.OFF}")
        return []


def parse_sitemap_xml_and_get_urls(sitemap_content: str | bytes | Any) -> list[str]:
    """Fastest method to parse the contents of an XML sitemap file, e.g. from a response, and retrieve all the URLs from it.

    Args:
        content (str | bytes | Any): The content of the XML sitemap file.

    Returns:
        list[str]: List of the URLs found in the XML sitemap file. If no URLs are found, the list will be empty.
    """

    try:
        sitemap_tree = lxml.etree.fromstring(sitemap_content)
        sitemap_urls = sitemap_tree.xpath("//ns:url/ns:loc/text()", namespaces=SITEMAP_SCHEMA_NAMESPACE)
        return [str(url).strip() for url in sitemap_urls] if isinstance(sitemap_urls, list) and sitemap_urls else []
    except Exception:
        print(f"{Color.YELLOW}Invalid sitemap format. The XML could not be parsed. Please check the location of the sitemap.{Color.OFF}")
        return []
