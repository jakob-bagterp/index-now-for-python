from enum import Enum, unique


@unique
class SearchEngineEndpoint(Enum):
    """Endpoint options for the IndexNow API. Reference: https://www.indexnow.org/faq"""

    INDEXNOW = "https://api.indexnow.org/"
    MICROSOFT_BING = "https://www.bing.com/"
    NAVER = "https://searchadvisor.naver.com/"
    SEZNAM = "https://search.seznam.cz/"
    YANDEX = "https://yandex.com/"
    YEP = "https://indexnow.yep.com/"

    def __str__(self) -> str:
        return str(self.value)
