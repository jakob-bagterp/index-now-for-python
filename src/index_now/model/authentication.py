from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class IndexNowAuthentication:
    """Authentication credentials for the IndexNow API.

    Args:
        host (str): The host of the website to be indexed, e.g. `example.com`.
        api_key (str): The IndexNow API key, e.g. `a1b2c3d4`.
        api_key_location (str): The URL of the IndexNow API key file, e.g. `https://example.com/a1b2c3d4.txt`.

    Example:
        Basic usage:

        ```python linenums="1" hl_lines="3-7"
        from index_now import submit_url_to_index_now, IndexNowAuthentication

        authentication = IndexNowAuthentication(
            host="example.com",
            api_key="a1b2c3d4",
            api_key_location="https://example.com/a1b2c3d4.txt",
        )

        submit_url_to_index_now(authentication, "https://example.com/page1")
        ```
    """

    host: str
    api_key: str
    api_key_location: str
