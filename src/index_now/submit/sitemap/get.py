from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from typing import Any

from ...constant.cpu import NUMBER_OF_CPU_CORES
from ...utility import http_client


def get_sitemap_xml(sitemap_location: str, retries: int = 0) -> str | bytes | Any:
    """Get the contents of an XML sitemap file.

    Args:
        sitemap_location (str): The location of the sitemap to get the URLs from.
        retries (int): Number of retries to use when requesting the sitemap.

    Returns:
        str | bytes | Any: The sitemap content, or an empty string if the sitemap could not be retrieved.

    Raises:
        RequestException: If the request fails or the response has an error status.
    """

    if not sitemap_location:
        return ""

    response = http_client.get(sitemap_location, retries=retries)
    response.raise_for_status()
    return response.content


def get_multiple_sitemap_xml(sitemap_locations: list[str], retries: int = 0) -> list[str | bytes | Any]:
    """Get the contents of multiple XML sitemaps in parallel.

    Args:
        sitemap_locations (list[str]): List of sitemap locations to get the URLs from.
        retries (int): Number of retries to use when requesting each sitemap.

    Returns:
        list[str | bytes | Any]: The sitemap contents, or an empty string if the sitemap could not be retrieved.

    Raises:
        RequestException: If any request fails or has an error status.
    """

    # Quick exits if there are no or only one sitemap location to process:
    if not sitemap_locations:
        return []
    if len(sitemap_locations) == 1:
        return [get_sitemap_xml(sitemap_locations[0], retries=retries)]

    max_workers = min(max(1, NUMBER_OF_CPU_CORES - 1), len(sitemap_locations))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        multiple_contents = list(executor.map(get_sitemap_xml, sitemap_locations, repeat(retries)))

    return multiple_contents
