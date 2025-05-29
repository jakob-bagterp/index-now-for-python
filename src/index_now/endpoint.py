from enum import Enum, unique


@unique
class SearchEngineEndpoint(Enum):
    """Endpoint options for the [IndexNow API](https://www.indexnow.org/faq).

    Attributes:
        SearchEngineEndpoint.INDEXNOW (Enum): [IndexNow](https://www.indexnow.org) default endpoint.
        SearchEngineEndpoint.BING (Enum): [Microsoft Bing](https://www.bing.com).
        SearchEngineEndpoint.NAVER (Enum): [Naver](https://www.naver.com).
        SearchEngineEndpoint.SEZNAM (Enum): [Seznam.cz](https://www.seznam.cz).
        SearchEngineEndpoint.YANDEX (Enum): [Yandex](https://yandex.com).
        SearchEngineEndpoint.YEP (Enum): [Yep](https://yep.com).

    Example:
        How to submit a URL to the IndexNow API using different endpoint options or a custom endpoint:

        ```python linenums="1" hl_lines="9-14"
        from index_now import submit_url_to_index_now, IndexNowAuthentication, SearchEngineEndpoint

        authentication = IndexNowAuthentication(
            host="example.com",
            api_key="a1b2c3d4",
            api_key_location="https://example.com/a1b2c3d4.txt",
        )

        endpoint_bing = SearchEngineEndpoint.BING
        endpoint_yandex = SearchEngineEndpoint.YANDEX
        endpoint_custom = "https://example.com/indexnow"

        for endpoint in [endpoint_bing, endpoint_yandex, endpoint_custom]:
            submit_url_to_index_now(authentication, "https://example.com/page1", endpoint)
        ```
    """

    INDEXNOW = "https://api.indexnow.org/indexnow"
    BING = "https://www.bing.com/indexnow"
    NAVER = "https://searchadvisor.naver.com/indexnow"
    SEZNAM = "https://search.seznam.cz/indexnow"
    YANDEX = "https://yandex.com/indexnow"
    YEP = "https://indexnow.yep.com/indexnow"

    def __str__(self) -> str:
        return str(self.value)
