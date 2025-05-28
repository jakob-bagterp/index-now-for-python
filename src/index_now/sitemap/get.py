from typing import Any

import requests


def get_sitemap_xml(sitemap_location: str) -> str | bytes | Any:
    """Get the contents of a sitemap.xml file.

    Args:
        sitemap_location (str): The URL of the sitemap to get the URLs from.

    Returns:
        str | bytes | Any: The contents of the sitemap.xml file, or empty string if no URLs are found.
    """

    response = requests.get(sitemap_location)
    return response.content
