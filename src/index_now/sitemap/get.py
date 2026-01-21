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

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(get_sitemap_xml, sitemap_locations))

    return results
