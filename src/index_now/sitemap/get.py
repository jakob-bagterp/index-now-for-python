import requests

from .parse import parse_sitemap_xml_and_get_urls


def get_urls_from_sitemap_xml(sitemap_location: str) -> list[str]:
    """Get all URLs from a sitemap.xml file.

    Args:
        sitemap_location (str): The URL of the sitemap to get the URLs from.

    Returns:
        list[str] | None: List of URLs found in the sitemap.xml file, or empty list if no URLs are found.
    """

    response = requests.get(sitemap_location)
    return parse_sitemap_xml_and_get_urls(response.content)
