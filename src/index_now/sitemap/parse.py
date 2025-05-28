from dataclasses import dataclass
from typing import Any

import lxml.etree
from colorist import Color


@dataclass(slots=True, frozen=True)
class SitemapUrl:
    """Reprensents an `<url>...</url>` element in a sitemap XML file so it can be parsed in a data structure.

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


def parse_sitemap_xml_and_get_urls(sitemap_content: str | bytes | Any) -> list[str]:
    """Parse the contents of a sitemap.xml file, e.g. from a response, and retrieve all the URLs from it.

    Args:
        content (str | bytes | Any): The content from the sitemap.xml file.

    Returns:
        list[str]: List of URLs found in the sitemap.xml file, or empty list if no URLs are found.
    """

    try:
        sitemap_tree = lxml.etree.fromstring(sitemap_content)
        sitemap_urls = sitemap_tree.xpath("//ns:url/ns:loc/text()", namespaces={"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"})
        return [str(url).strip() for url in sitemap_urls] if isinstance(sitemap_urls, list) and sitemap_urls else []
    except Exception:
        print(f"{Color.YELLOW}Invalid sitemap.xml format during parsing. Please check the sitemap location.{Color.OFF}")
        return []
