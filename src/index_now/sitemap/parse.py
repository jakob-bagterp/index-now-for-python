from dataclasses import dataclass
from enum import StrEnum, auto, unique
from typing import Any

import lxml.etree
from colorist import Color


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


@unique
class SitemapElementType(StrEnum):
    SITEMAP = auto()
    URL = auto()


SITEMAP_SCHEMA_NAMESPACE = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def parse_sitemap_xml_and_get_xpath_objects(sitemap_content: str | bytes | Any, type: SitemapElementType, loc_only: bool) -> Any:
    """Parse the contents of an XML sitemap file and get the URLs or nested XML sitemaps from it.

    Args:
        content (str | bytes | Any): The content of the XML sitemap file.
        type (SitemapElementType): Type of sitemap element to parse, e.g. URL or a nested XML sitemap.
        loc_only (bool): Return only the location/URL of the sitemap element or all the sitemap element attributes for further processing.

    Returns:
        _XPathObject: The XPath object containing the URLs or nested XML sitemap. If no elements are found, the XPath object will be empty.
    """

    def define_xpath(type: SitemapElementType, loc_only: bool) -> str:
        base_xpath = f"//ns:{type}"
        return f"{base_xpath}/ns:loc/text()" if loc_only else base_xpath

    xpath = define_xpath(type, loc_only)
    sitemap_tree = lxml.etree.fromstring(sitemap_content)
    return sitemap_tree.xpath(xpath, namespaces=SITEMAP_SCHEMA_NAMESPACE)


def parse_sitemap_xml_and_get_urls_as_elements(sitemap_content: str | bytes | Any) -> list[SitemapUrl]:
    """Parse the contents of an XML sitemap file, e.g. from a response, and retrieve all the URLs from it as `SitemapUrl` elements.

    Args:
        content (str | bytes | Any): The content of the XML sitemap file.

    Returns:
        list[SitemapUrl]: List of SitemapUrl objects found in the XML sitemap file, or empty list if no URLs are found.
    """

    try:
        urls: list[SitemapUrl] = []
        sitemap_elements = parse_sitemap_xml_and_get_xpath_objects(sitemap_content, SitemapElementType.URL, loc_only=False)
        for sitemap_element in sitemap_elements:
            loc = sitemap_element.xpath("ns:loc/text()", namespaces=SITEMAP_SCHEMA_NAMESPACE)[0].strip()
            lastmod = next(iter(sitemap_element.xpath("ns:lastmod/text()", namespaces=SITEMAP_SCHEMA_NAMESPACE)), None)
            changefreq = next(iter(sitemap_element.xpath("ns:changefreq/text()", namespaces=SITEMAP_SCHEMA_NAMESPACE)), None)
            priority = next(iter(sitemap_element.xpath("ns:priority/text()", namespaces=SITEMAP_SCHEMA_NAMESPACE)), None)
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
        sitemap_urls = parse_sitemap_xml_and_get_xpath_objects(sitemap_content, SitemapElementType.URL, loc_only=True)
        return [str(url).strip() for url in sitemap_urls] if isinstance(sitemap_urls, list) and sitemap_urls else []
    except Exception:
        print(f"{Color.YELLOW}Invalid sitemap format. The XML could not be parsed. Please check the location of the sitemap.{Color.OFF}")
        return []
