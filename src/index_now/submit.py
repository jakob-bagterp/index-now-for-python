import requests

from .authentication import IndexNowAuthentication


def submit_urls_to_index_now(authentication: IndexNowAuthentication, urls: list[str]) -> None:
    """Submits a list of URLs to the Bing's IndexNow API.

    Args:
        authentication (IndexNowAuthentication): Authentication data for the IndexNow API.
        urls (list[str]): List of URLs to submit, e.g. `["https://example.com/page1", "https://example.com/page2"]`.
    """

    payload: dict[str, str | list[str]] = {
        "host": authentication.host,
        "key": authentication.api_key,
        "keyLocation": authentication.api_key_location,
        "urlList": urls
    }
    response = requests.post(
        url="api.indexnow.org",
        json=payload,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

    if response.status_code == 200:
        print(f"Sitemap of {len(urls)} URL(s) submitted successfully.")
    else:
        print(f"Failed to submit sitemap. Status code: {response.status_code}, Response: {response.text}")
