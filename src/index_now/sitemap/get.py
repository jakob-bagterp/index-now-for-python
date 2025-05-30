from typing import Any

import requests


def get_sitemap_xml(sitemap_location: str) -> str | bytes | Any:
    """Get the contents of an XML sitemap file.

    Args:
        sitemap_location (str): The location of the sitemap to get the URLs from.

    Returns:
        str | bytes | Any: The contents of the XML sitemp file or an empty string if the sitemap could not be retrieved.
    """

    response = requests.get(sitemap_location)
    return response.content
