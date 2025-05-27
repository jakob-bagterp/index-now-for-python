from enum import Enum, unique


@unique
class ChangeFrequency(Enum):
    """The change frequency of a sitemap URL, e.g. `<changefreq>monthly</changefreq>`, and is used to indicate to a crawler how often the resource is expected to change. Reference: https://www.sitemaps.org/protocol.html#xmlTagDefinitions"""

    ALWYAS = "always"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    NEVER = "never"
