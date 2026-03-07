from concurrent.futures import ProcessPoolExecutor
from typing import Any

import requests


def get_sitemap_xml(sitemap_location: str) -> str | bytes | Any:
    """Get the contents of an XML sitemap file.

    Args:
        sitemap_location (str): The location of the sitemap to get the URLs from.

    Returns:
        str | bytes | Any: The contents of the XML sitemp file or an empty string if the sitemap could not be retrieved.
    """

    if not sitemap_location:
        return ""

    try:
        response = requests.get(sitemap_location, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception:
        return ""


def get_multiple_sitemap_xml(sitemap_locations: list[str], max_workers: int | None = None) -> list[str | bytes | Any]:
    """Get the contents of multiple XML sitemaps in parallel.

    Args:
        sitemap_locations (list[str]): List of sitemap locations to get the URLs from.
        max_workers (int | None, optional): Maximum number of workers to use for parallel processing. If `None`, the number of available CPU cores will be used.

    Returns:
        list[str | bytes | Any]: List of the contents of the XML sitemap files or an empty list if the sitemaps could not be retrieved.
    """

    # Quick exits if there are no or only one sitemap location to process:
    if not sitemap_locations:
        return []
    if len(sitemap_locations) == 1:
        return [get_sitemap_xml(sitemap_locations[0])]

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        multiple_contents = list(executor.map(get_sitemap_xml, sitemap_locations))

    return multiple_contents
