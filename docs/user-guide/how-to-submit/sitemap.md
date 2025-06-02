---
title: How to Submit a Sitemap or Multiple Sitemaps
description: Learn how to submit an entire sitemap of multiple URLs to the IndexNow API to get your website indexed faster by search engines. Includes code examples for beginners and advanced users.
tags:
    - Tutorial
    - Sitemap
    - Filtering
    - Last Modified
    - Date Range
    - Change Frequency
---

# How to Submit All Sitemap URLs in Bulk to IndexNow
## Single Sitemap
If several pages on your site have changed and you want them all to be reindexed, you can submit an entire sitemap of multiple URLs to the IndexNow API using the [`submit_sitemap_to_index_now()`](../../reference/methods/submit-sitemap.md) method:

```python linenums="1" hl_lines="9"
from index_now import submit_sitemap_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

submit_sitemap_to_index_now(authentication, "https://example.com/sitemap.xml")
```

!!! info
    What happens when submitting a sitemap with IndexNow for Python:

    1. Downloads the specified sitemap(s)
    2. Parses the sitemap(s) and extracts the URLs
    3. If any filters applied, filters the list of URLs to be submitted
    4. Submits the (filtered) URLs to the IndexNow API

    The IndexNow API will then process the URLs and return the results.

## Multiple Sitemaps
If you have multiple sitemaps, you can submit them all at once using the [`submit_sitemaps_to_index_now()`](../../reference/methods/submit-multiple-sitemaps.md) method:

```python linenums="1" hl_lines="9-15"
from index_now import submit_sitemaps_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

sitemap_locations = [
    "https://example.com/sitemap1.xml",
    "https://example.com/sitemap2.xml",
    "https://example.com/sitemap3.xml",
]

submit_sitemaps_to_index_now(authentication, sitemap_locations)
```

## How to Filter the URLs
Sometimes, you may wish to submit only a subset of the URLs in a sitemap. This could be URLs that have changed recently, URLs that have changed within a given timeframe, URLs that contain a specific text or even just a subset of URLs. The [`SitemapFilter` configuration class](../../reference/sitemap-filter/sitemap-filter.md) gives you that flexibility.

For example:

```python linenums="1" hl_lines="9"
from index_now import submit_sitemap_to_index_now, IndexNowAuthentication, SitemapFilter

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

filter = SitemapFilter(contains="section1", skip=2, take=3)

submit_sitemap_to_index_now(authentication,
    "https://example.com/sitemap.xml", filter)
```

The same applies to submitting multiple sitemaps:

```python linenums="1" hl_lines="15"
from index_now import submit_sitemaps_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

sitemap_locations = [
    "https://example.com/sitemap1.xml",
    "https://example.com/sitemap2.xml",
    "https://example.com/sitemap3.xml",
]

filter = SitemapFilter(contains="section1", skip=2, take=3)

submit_sitemaps_to_index_now(authentication,
    sitemap_locations, filter)
```

### By Change Frequency
Before submitting the sitemap to IndexNow, you can also target URLs with a specific `<changefreq>` value using the `change_frequency` parameter. Either use the predefined [`ChangeFrequency`](../../reference/sitemap-filter/change-frequency.md) enumerations:

```python linenums="1" hl_lines="3"
from index_now import SitemapFilter, ChangeFrequency

filter = SitemapFilter(change_frequency=ChangeFrequency.DAILY)
```

Or use a basic string input:

```python linenums="1" hl_lines="3"
from index_now import SitemapFilter

filter = SitemapFilter(change_frequency="daily")
```

### By Date Range
The `date_range` parameter filters the `<lastmod>` elements of the sitemap entries, enabling you to select URLs modified within a specific date range.

The [`DateRange` and its many sibling classes](../../reference/sitemap-filter/date-range.md) make it easy to target URLs with a specific `<lastmod>` date. For example:

```python linenums="1" hl_lines="4-7"
from datetime import datetime
from index_now import DateRange, SitemapFilter

january_2025 = DateRange(
    start=datetime(2025, 1, 1),
    end=datetime(2025, 1, 31),
)

filter = SitemapFilter(date_range=january_2025)
```

Instead of using absolute dates, you can use relative ranges. For example, you can use the `DaysAgo` parameter to target URLs that have been modified recently:

```python linenums="1" hl_lines="3"
from index_now import DaysAgo, SitemapFilter

two_days_ago = DaysAgo(2)

filter = SitemapFilter(date_range=two_days_ago)
```

### By Text
You can limit the sitemap URLs to only those containing a specific text using the `contains` parameter of the [`SitemapFilter`](../../reference/sitemap-filter/sitemap-filter.md):

```python linenums="1" hl_lines="3"
from index_now import SitemapFilter

filter = SitemapFilter(contains="section1")
```

Or exclude URLs that contain a specific text using the `excludes` parameter:

```python linenums="1" hl_lines="3"
from index_now import SitemapFilter

filter = SitemapFilter(excludes="page1")
```

#### Pattern or Regular Expression
The `contains` parameter also accepts regular expressions for more advanced filtering. For example, if you want to match URLs that contain either `section1` or `section2`, you can use the regular expression `r"(section1)|(section2)"`:

```python linenums="1" hl_lines="3"
from index_now import SitemapFilter

filter = SitemapFilter(contains=r"(section1)|(section2)")
```

Similarly, the `excludes` parameter can be used to exclude URLs that match a specific regular expression:

```python linenums="1" hl_lines="3"
from index_now import SitemapFilter

filter = SitemapFilter(excludes=r"(page1)|(page2)")
```

### By Amount: Skip and Take
Let's imagine a sitemap with a 100 URLs. You don't want to submit everything, so you can use the `skip` and `take` parameters to skip the first 10 URLs and submit the next 20 URLs:

```python linenums="1" hl_lines="3"
from index_now import SitemapFilter

filter = SitemapFilter(skip=10, take=20)
```

### Order of Filtering Rules
!!! tip
    When using multiple filtering options at the same time, be aware of the order of the filtering rules. You don't have to use every rule, but each rule can reduce the pool of URLs before passing them on to the next filter.

All of these parameters can be combined in the same filter. But the order of the parameters in the [`SitemapFilter` configuration class](../../reference/sitemap-filter/sitemap-filter.md) is also the order in which the filtering rules will be applied:

```python
from index_now import SitemapFilter

filter = SitemapFilter(
    change_frequency="daily",
    date_range=DaysAgo(2),
    contains="section1",
    excludes="search",
    skip=1,
    take=1
)
```

#### Example
Let's imagine a sitemap with 9 URLs, the order of the `contains`, `skip`, and `take` parameters will filter the URLs like this:

| `sitemap.xml`   | `contains="section1"` | `skip=1`        | `take=1`        |
| --------------- | --------------------- | --------------- | --------------- |
| /page1          |                       |                 |                 |
| /page2          |                       |                 |                 |
| /page3          |                       |                 |                 |
| /section1/page1 | /section1/page1       |                 |                 |
| /section1/page2 | /section1/page2       | /section1/page2 | /section1/page2 |
| /section1/page3 | /section1/page3       | /section1/page3 |                 |
| /section2/page1 |                       |                 |                 |
| /section2/page2 |                       |                 |                 |
| /section2/page3 |                       |                 |                 |
