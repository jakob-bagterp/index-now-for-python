from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class IndexNowAuthentication:
    """Authentication data for the IndexNow API.

    Args:
        host (str): The host of the website to be indexed, e.g. `example.com`.
        api_key (str): The IndexNow API key, e.g. `a1b2c3d4`.
        api_key_location (str): The URL of the IndexNow API key file, e.g. `https://example.com/a1b2c3d4.txt`.
    """

    host: str
    api_key: str
    api_key_location: str
