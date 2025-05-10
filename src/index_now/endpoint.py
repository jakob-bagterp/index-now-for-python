from enum import Enum, unique


@unique
class SearchEngineEndpoint(Enum):
    """Endpoint options for the IndexNow API. Reference: https://www.indexnow.org/faq"""

    INDEXNOW = "https://api.indexnow.org/"
    MICROSOFT_BING = "https://www.bing.com/indexnow"
    NAVER = "https://searchadvisor.naver.com/indexnow"
    SEZNAM = "https://search.seznam.cz/indexnow"
    YANDEX = "https://yandex.com/indexnow"
    YEP = "https://indexnow.yep.com/indexnow"

    def __str__(self) -> str:
        return str(self.value)
