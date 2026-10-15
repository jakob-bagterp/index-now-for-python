from enum import Enum, unique


@unique
class ChangeFrequency(Enum):
    """The change frequency of a sitemap URL, e.g. `<changefreq>monthly</changefreq>`, and is used to indicate to a crawler how often the resource is expected to change. Find more inforation at [www.sitemaps.org](https://www.sitemaps.org/protocol.html#xmlTagDefinitions).

    Attributes:
        ChangeFrequency.ALWAYS (Enum): The resource is always changing.
        ChangeFrequency.HOURLY (Enum): The resource changes every hour.
        ChangeFrequency.DAILY (Enum): The resource changes every day.
        ChangeFrequency.WEEKLY (Enum): The resource changes every week.
        ChangeFrequency.MONTHLY (Enum): The resource changes every month.
        ChangeFrequency.YEARLY (Enum): The resource changes every year.
        ChangeFrequency.NEVER (Enum): The resource never changes.

    Example:
        Get all URLs with a change frequency set to `daily`:

        ```python linenums="1" hl_lines="3"
        from index_now import SitemapFilter, ChangeFrequency

        filter = SitemapFilter(change_frequency=ChangeFrequency.DAILY)
        ```

        Instead of the predefined `ChangeFrequency` enumerations, you can also use basic string input:

        ```python linenums="3" hl_lines="1" title=""
        filter = SitemapFilter(change_frequency="daily")
        ```
    """

    ALWAYS = "always"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    NEVER = "never"

    def __str__(self) -> str:
        return str(self.value.lower())
