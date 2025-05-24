import requests
from colorist import Color

from .authentication import IndexNowAuthentication
from .endpoint import SearchEngineEndpoint

ACCEPTED_STATUS_CODES = [200, 202]


def submit_url_to_index_now(authentication: IndexNowAuthentication, url: str, endpoint: SearchEngineEndpoint | str = SearchEngineEndpoint.INDEXNOW) -> int:
    """Submits a list of URLs to the IndexNow API of a search engine.

    Args:
        authentication (IndexNowAuthentication): Authentication credentials for the IndexNow API.
        url (str): URL to submit, e.g. `"https://example.com/page1"`.
        endpoint (SearchEngineEndpoint | str, optional): Select the search engine you want to submit to or use a custom URL as endpoint.

    Returns:
        int: Status code of the response, e.g. `200` or `202` for, respectively, success or accepted, or `400` for bad request, etc.

    Example:
        After adding your authentication credentials to the `IndexNowAuthentication` class, you can now submit a single URL to the IndexNow API:

        ```python linenums="1" hl_lines="11"
        from index_now import submit_url_to_index_now, IndexNowAuthentication

        authentication = IndexNowAuthentication(
            host="example.com",
            api_key="a1b2c3d4",
            api_key_location="https://example.com/a1b2c3d4.txt",
        )

        url = "https://example.com/page1"

        submit_url_to_index_now(authentication, url)
        ```

        If you want to submit to a specific search engine, alternatively customize the endpoint:

        ```python linenums="11" hl_lines="1-2" title=""
        submit_url_to_index_now(authentication, url,
            endpoint="https://www.bing.com/indexnow")
        ```
    """

    response = requests.get(url=str(endpoint), params={"url": url, "key": authentication.api_key, "keyLocation": authentication.api_key_location})

    if response.status_code in ACCEPTED_STATUS_CODES:
        print(f"{Color.GREEN}URL submitted successfully to the IndexNow API:{Color.OFF} {endpoint}")
        print(f"Status code: {Color.GREEN}{response.status_code}{Color.OFF}")
    else:
        print("Failed to submit URL.")
        print(f"Status code: {Color.RED}{response.status_code}{Color.OFF}. Response: {response.text}")
    return response.status_code


def submit_urls_to_index_now(authentication: IndexNowAuthentication, urls: list[str], endpoint: SearchEngineEndpoint | str = SearchEngineEndpoint.INDEXNOW) -> int:
    """Submits a list of URLs to the IndexNow API of a search engine.

    Args:
        authentication (IndexNowAuthentication): Authentication credentials for the IndexNow API.
        urls (list[str]): List of URLs to submit. For example: `["https://example.com/page1", "https://example.com/page2", "https://example.com/page3"]`
        endpoint (SearchEngineEndpoint | str, optional): Select the search engine you want to submit to or use a custom URL as endpoint.

    Returns:
        int: Status code of the response, e.g. `200` or `202` for, respectively, success or accepted, or `400` for bad request, etc.

    Example:
        After adding your authentication credentials to the `IndexNowAuthentication` class, you can now submit multiple URLs to the IndexNow API:

        ```python linenums="1" hl_lines="11"
        from index_now import submit_urls_to_index_now, IndexNowAuthentication

        authentication = IndexNowAuthentication(
            host="example.com",
            api_key="a1b2c3d4",
            api_key_location="https://example.com/a1b2c3d4.txt",
        )

        urls = ["https://example.com/page1", "https://example.com/page2", "https://example.com/page3"]

        submit_urls_to_index_now(authentication, urls)
        ```

        If you want to submit to a specific search engine, alternatively customize the endpoint:

        ```python linenums="11" hl_lines="1-2" title=""
        submit_urls_to_index_now(authentication, urls,
            endpoint="https://www.bing.com/indexnow")
        ```
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

    if response.status_code in ACCEPTED_STATUS_CODES:
        print(f"{Color.GREEN}{len(urls)} URL(s) submitted successfully to the IndexNow API:{Color.OFF} {endpoint}")
        print(f"Status code: {Color.GREEN}{response.status_code}{Color.OFF}")
    else:
        print("Failed to submit URL(s).")
        print(f"Status code: {Color.RED}{response.status_code}{Color.OFF}. Response: {response.text}")
    return response.status_code
