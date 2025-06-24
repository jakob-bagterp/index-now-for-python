import requests

from index_now import SearchEngineEndpoint
from index_now.status_code import StatusCodes

TEMPORARILY_SKIPPED_ENDPOINTS = [
    SearchEngineEndpoint.BING,
]


def is_endpoint_up(endpoint: SearchEngineEndpoint | str) -> bool:
    """According to the IndexNow documentation for search engines (https://www.indexnow.org/searchengines), the endpoint should always host a `meta.json` file, so this is a proxy to test whether the endpoint is up. Find a list of endpoints here: https://www.indexnow.org/searchengines.json"""

    try:
        response = requests.get(f"{endpoint}/meta.json")
        return response.status_code == StatusCodes.OK
    except Exception:  # pragma: no cover
        return False  # pragma: no cover
