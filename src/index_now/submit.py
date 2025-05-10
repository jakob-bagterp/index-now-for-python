import requests
from colorist import Color

from .authentication import IndexNowAuthentication
from .endpoint import SearchEngineEndpoint


def submit_urls_to_index_now(authentication: IndexNowAuthentication, urls: list[str], endpoint: SearchEngineEndpoint | str = SearchEngineEndpoint.INDEXNOW) -> None:
    """Submits a list of URLs to the IndexNow API of a search engine.

    Args:
        authentication (IndexNowAuthentication): Authentication data for the IndexNow API.
        urls (list[str]): List of URLs to submit, e.g. `["https://example.com/page1", "https://example.com/page2"]`.
        endpoint (SearchEngineEndpoint | str, optional): Select the search engine you want to submit to or use a custom URL as endpoint.
    """

    payload: dict[str, str | list[str]] = {
        "host": authentication.host,
        "key": authentication.api_key,
        "keyLocation": authentication.api_key_location,
        "urlList": urls
    }
    response = requests.post(
        url=str(endpoint),
        json=payload,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

    if response.status_code == 200:
        print(f"{Color.GREEN}{len(urls)} URL(s) submitted successfully to the IndexNow API:{Color.OFF} {endpoint}")
        print(f"Status code: {Color.GREEN}{response.status_code}{Color.OFF}")
    else:
        print("Failed to submit sitemap.")
        print(f"Status code: {Color.RED}{response.status_code}{Color.OFF}. Response: {response.text}")
