from collections.abc import Sequence

from ...model.authentication import IndexNowAuthentication
from ...model.endpoint import SearchEngineEndpoint
from ...utility import http_client
from ..fallback import submit_with_fallback


def submit_url_to_index_now(
    authentication: IndexNowAuthentication,
    url: str,
    endpoint: SearchEngineEndpoint | str | Sequence[SearchEngineEndpoint | str] = SearchEngineEndpoint.INDEXNOW,
    retries: int = 0,
) -> int:
    """Submit a list of URLs to the IndexNow API of a search engine.

    Args:
        authentication (IndexNowAuthentication): Authentication credentials for the IndexNow API.
        url (str): URL to submit, e.g. `"https://example.com/page1"`.
        endpoint (SearchEngineEndpoint | str | Sequence[SearchEngineEndpoint | str], optional): Select the search engine you want to submit to or use a custom URL as endpoint. If a list or tuple of endpoints is given, they are tried in order until one accepts the submission. The submission falls back to the next endpoint on connection errors, server errors, `429 Too Many Requests` and `403 Forbidden`, but not on other client errors such as `400 Bad Request`.
        retries (int, optional): Number of times to retry a request on connection errors, timeouts, `429 Too Many Requests` and server errors, with exponential backoff. Defaults to `0`, i.e. no retries. If a list or tuple of endpoints is given, each endpoint is retried before falling back to the next one.

    Returns:
        int: The status code of the response, e.g. `200` for success, `202` for accepted, `400` for bad request, etc. If a list or tuple of endpoints is given and all of them fail, the last response status is returned if any endpoint responded; otherwise, the final connection error or timeout is raised.

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

        Or provide a list of endpoints as fallback in case an endpoint is unavailable or rejects the submission. The endpoints are tried in order until one succeeds:

        ```python linenums="11" hl_lines="1-5 7" title=""
        endpoints_with_fallback = [
            "https://www.bing.com/indexnow",
            "https://yandex.com/indexnow",
            "https://search.seznam.cz/indexnow",
        ]

        submit_url_to_index_now(authentication, url, endpoint=endpoints_with_fallback)
        ```
    """

    return submit_with_fallback(
        endpoint,
        send=lambda endpoint_url: http_client.get(
            url=endpoint_url,
            retries=retries,
            params={"url": url, "key": authentication.api_key, "keyLocation": authentication.api_key_location},
        ),
        success_message="1 URL was submitted successfully to this IndexNow API endpoint:",
        failure_message="Failure. No URL was submitted to this IndexNow API endpoint:",
    )


def submit_urls_to_index_now(
    authentication: IndexNowAuthentication,
    urls: list[str],
    endpoint: SearchEngineEndpoint | str | Sequence[SearchEngineEndpoint | str] = SearchEngineEndpoint.INDEXNOW,
    retries: int = 0,
) -> int:
    """Submit a list of URLs to the IndexNow API of a search engine.

    Args:
        authentication (IndexNowAuthentication): Authentication credentials for the IndexNow API.
        urls (list[str]): List of URLs to submit. For example: `["https://example.com/page1", "https://example.com/page2", "https://example.com/page3"]`
        endpoint (SearchEngineEndpoint | str | Sequence[SearchEngineEndpoint | str], optional): Select the search engine you want to submit to or use a custom URL as endpoint. If a list or tuple of endpoints is given, they are tried in order until one accepts the submission. The submission falls back to the next endpoint on connection errors, server errors, `429 Too Many Requests` and `403 Forbidden`, but not on other client errors such as `400 Bad Request`.
        retries (int, optional): Number of times to retry a request on connection errors, timeouts, `429 Too Many Requests` and server errors, with exponential backoff. Defaults to `0`, i.e. no retries. If a list or tuple of endpoints is given, each endpoint is retried before falling back to the next one.

    Returns:
        int: The status code of the response, e.g. `200` for success, `202` for accepted, `400` for bad request, etc. If a list or tuple of endpoints is given and all of them fail, the last response status is returned if any endpoint responded; otherwise, the final connection error or timeout is raised.

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

        Or provide a list of endpoints as fallback in case an endpoint is unavailable or rejects the submission. The endpoints are tried in order until one succeeds:

        ```python linenums="11" hl_lines="1-5 7" title=""
        endpoints_with_fallback = [
            "https://www.bing.com/indexnow",
            "https://yandex.com/indexnow",
            "https://search.seznam.cz/indexnow",
        ]

        submit_urls_to_index_now(authentication, urls, endpoint=endpoints_with_fallback)
        ```
    """

    payload: dict[str, str | list[str]] = {
        "host": authentication.host,
        "key": authentication.api_key,
        "keyLocation": authentication.api_key_location,
        "urlList": urls,
    }
    return submit_with_fallback(
        endpoint,
        send=lambda endpoint_url: http_client.post(
            url=endpoint_url, retries=retries, json=payload, headers={"Content-Type": "application/json; charset=utf-8"}
        ),
        success_message=f"{len(urls):,} URL(s) were submitted successfully to this IndexNow API endpoint:",
        failure_message="Failure. No URL(s) were submitted to this IndexNow API endpoint:",
    )
