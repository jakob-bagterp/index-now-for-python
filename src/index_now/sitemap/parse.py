from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SitemapUrl:
    """Reprensents an `<url>...</url>` element in a sitemap XML file so it can be parsed in a data structure.

    Attributes:
        loc (str): The location of the URL.
        lastmod (str | None): The last modification date of the URL. Optional.
        changefreq (str | None): The change frequency of the URL. Optional.
        priority (float | None): The priority of the URL. Optional.
    """

    loc: str
    lastmod: str | None = None
    changefreq: str | None = None
    priority: float | None = None
