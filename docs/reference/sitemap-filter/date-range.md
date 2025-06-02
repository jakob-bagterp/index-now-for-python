---
title: Documentation of Date Range Filter Settings
description: Learn how to use date range options to filter URLs from a sitemap before submitting them in bulk to IndexNow. Includes code examples for beginners and advanced users.
tags:
    - Documentation
    - Tutorial
    - Sitemap
    - Filtering
    - Date Range
    - Last Modified
---

# Date Range Filter Options
## Example
The date range of the [`SitemapFilter`](sitemap-filter.md) is a powerful way to control which URLs are submitted to IndexNow based on their `<lastmod>` date. This is particularly useful for ensuring that only relevant and recent content is submitted.

Let's image that we have a sitemap with three URLs, each with different last modified dates:

```xml linenums="1" title="sitemap.xml" hl_lines="5 11 17"
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://example.com</loc>
        <lastmod>2025-01-01</lastmod>
        <changefreq>always</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://example.com/page1</loc>
        <lastmod>2025-02-01</lastmod>
        <changefreq>hourly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://example.com/page2</loc>
        <lastmod>2025-03-01</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.5</priority>
    </url>
</urlset>
```

Using the `LaterThanAndIncluding` date range, we can target any URLs with a last modified date of March 1, 2025 or later:

```python linenums="1" hl_lines="4-5"
from datetime import datetime
from index_now import LaterThanAndIncluding, SitemapFilter, submit_sitemap_to_index_now, IndexNowAuthentication

march_2025_or_later = LaterThanAndIncluding(datetime(2025, 3, 1))
filter = SitemapFilter(date_range=march_2025_or_later)

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

submit_sitemap_to_index_now(
    authentication, "https://example.com/sitemap.xml", filter)
```

This will effectively filter out URLs outside of this date range, ensuring that only the URL  `https://example.com/page2` is submitted to IndexNow.

## Documentation
### `DateRange`
::: index_now.sitemap.filter.date_range.DateRange
    options:
        members: false

### `Between`
::: index_now.sitemap.filter.date_range.Between
    options:
        members: false

### `Today`
::: index_now.sitemap.filter.date_range.Today
    options:
        members: false

### `Yesterday`
::: index_now.sitemap.filter.date_range.Yesterday
    options:
        members: false

### `Day`
::: index_now.sitemap.filter.date_range.Day
    options:
        members: false

### `DaysAgo`
::: index_now.sitemap.filter.date_range.DaysAgo
    options:
        members: false

### `LaterThan`
::: index_now.sitemap.filter.date_range.LaterThan
    options:
        members: false

### `LaterThanAndIncluding`
::: index_now.sitemap.filter.date_range.LaterThanAndIncluding
    options:
        members: false

### `EarlierThan`
::: index_now.sitemap.filter.date_range.EarlierThan
    options:
        members: false

### `EarlierThanAndIncluding`
::: index_now.sitemap.filter.date_range.EarlierThanAndIncluding
    options:
        members: false
