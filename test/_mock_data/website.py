from dataclasses import dataclass

from index_now import IndexNowAuthentication


@dataclass
class IndexNowWebsiteData:
    authentication: IndexNowAuthentication
    sitemap_url: str


TIMER_FOR_PYTHON = IndexNowWebsiteData(
    authentication=IndexNowAuthentication(
        host="https://jakob-bagterp.github.io/timer-for-python",
        api_key="6d71a14ac15c4c41a0c19e641f659208",
        api_key_location="https://jakob-bagterp.github.io/timer-for-python/assets/index-now/api-key.txt/",
    ),
    sitemap_url="https://jakob-bagterp.github.io/timer-for-python/sitemap.xml",
)

COLORIST_FOR_PYTHON = IndexNowWebsiteData(
    authentication=IndexNowAuthentication(
        host="https://jakob-bagterp.github.io/colorist-for-python",
        api_key="42a119a493b24c8f915bb44ec4c86714",
        api_key_location="https://jakob-bagterp.github.io/colorist-for-python/assets/index-now/api-key.txt/",
    ),
    sitemap_url="https://jakob-bagterp.github.io/colorist-for-python/sitemap.xml",
)

BROWSERIST = IndexNowWebsiteData(
    authentication=IndexNowAuthentication(
        host="https://jakob-bagterp.github.io/browserist",
        api_key="a739958823fa49b1a36350a90c4ed9d9",
        api_key_location="https://jakob-bagterp.github.io/browserist/assets/index-now/api-key.txt/",
    ),
    sitemap_url="https://jakob-bagterp.github.io/browserist/sitemap.xml",
)
