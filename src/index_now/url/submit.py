import requests
from colorist import Color

from ..authentication import IndexNowAuthentication
from ..endpoint import SearchEngineEndpoint

SUCCESS_STATUS_CODES_DICT = {200: "OK", 202: "Accepted"}

SUCCESS_STATUS_CODES = [status_code for status_code in SUCCESS_STATUS_CODES_DICT.keys()]


def submit_url_to_index_now(authentication: IndexNowAuthentication, url: str, endpoint: SearchEngineEndpoint | str = SearchEngineEndpoint.INDEXNOW) -> int:
    """Submit a list of URLs to the IndexNow API of a search engine.

    Args:
        authentication (IndexNowAuthentication): Authentication credentials for the IndexNow API.
        url (str): URL to submit, e.g. `"https://example.com/page1"`.
        endpoint (SearchEngineEndpoint | str, optional): Select the search engine you want to submit to or use a custom URL as endpoint.

    Returns:
        int: The status code of the response, e.g. `200` for success, `202` for accepted, `400` for bad request, etc.

    Example:
        After adding your authentication credentials to the [`IndexNowAuthentication`](../configuration/authentication.md) class, you can now submit a single URL to the IndexNow API:

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

    if response.status_code in SUCCESS_STATUS_CODES:
        print(f"{Color.GREEN}1 URL was submitted successfully to this IndexNow API endpoint:{Color.OFF} {endpoint}")
        print(f"Status code: {Color.GREEN}{response.status_code} {SUCCESS_STATUS_CODES_DICT[response.status_code]}{Color.OFF}")
    else:
        print(f"{Color.YELLOW}Failure. No URL was submitted to this IndexNow API endpoint:{Color.OFF} {endpoint}")
        print(f"Status code: {Color.RED}{response.status_code}{Color.OFF}")
        print(f"Response: {response.text}")
    return response.status_code


def submit_urls_to_index_now(authentication: IndexNowAuthentication, urls: list[str], endpoint: SearchEngineEndpoint | str = SearchEngineEndpoint.INDEXNOW) -> int:
    """Submit a list of URLs to the IndexNow API of a search engine.

    Args:
        authentication (IndexNowAuthentication): Authentication credentials for the IndexNow API.
        urls (list[str]): List of URLs to submit. For example: `["https://example.com/page1", "https://example.com/page2", "https://example.com/page3"]`
        endpoint (SearchEngineEndpoint | str, optional): Select the search engine you want to submit to or use a custom URL as endpoint.

    Returns:
        int: The status code of the response, e.g. `200` for success, `202` for accepted, `400` for bad request, etc.

    Example:
        After adding your authentication credentials to the [`IndexNowAuthentication`](../configuration/authentication.md) class, you can now submit multiple URLs to the IndexNow API:

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

    if response.status_code in SUCCESS_STATUS_CODES:
        print(f"{Color.GREEN}{len(urls):,} URL(s) were submitted successfully to this IndexNow API endpoint:{Color.OFF} {endpoint}")
        print(f"Status code: {Color.GREEN}{response.status_code} {SUCCESS_STATUS_CODES_DICT[response.status_code]}{Color.OFF}")
    else:
        print(f"{Color.YELLOW}Failure. No URL(s) were submitted to this IndexNow API endpoint:{Color.OFF} {endpoint}")
        print(f"Status code: {Color.RED}{response.status_code}{Color.OFF}")
        print(f"Response: {response.text}")
    return response.status_code
