from dataclasses import dataclass

from index_now import IndexNowAuthentication


@dataclass(slots=True, frozen=True)
class IndexNowWebsiteData:
    authentication: IndexNowAuthentication
    sitemap_url: str


GITHUB_PAGES_AUTHENTICATION = IndexNowAuthentication(
    host="jakob-bagterp.github.io",
    api_key="6d71a14ac15c4c41a0c19e641f659208",
    api_key_location="https://jakob-bagterp.github.io/index-now-api-key.txt",
)

TIMER_FOR_PYTHON = IndexNowWebsiteData(
    authentication=GITHUB_PAGES_AUTHENTICATION,
    sitemap_url="https://jakob-bagterp.github.io/timer-for-python/sitemap.xml",
)

COLORIST_FOR_PYTHON = IndexNowWebsiteData(
    authentication=GITHUB_PAGES_AUTHENTICATION,
    sitemap_url="https://jakob-bagterp.github.io/colorist-for-python/sitemap.xml",
)

BROWSERIST = IndexNowWebsiteData(
    authentication=GITHUB_PAGES_AUTHENTICATION,
    sitemap_url="https://jakob-bagterp.github.io/browserist/sitemap.xml",
)


INDEX_NOW_FOR_PYTHON = IndexNowWebsiteData(
    authentication=GITHUB_PAGES_AUTHENTICATION,
    sitemap_url="https://jakob-bagterp.github.io/index-now-for-python/sitemap.xml",
)
