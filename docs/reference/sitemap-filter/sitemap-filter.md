---
title: Documentation for Sitemap Filter Settings
description: Learn how to filter URLs from a sitemap before submitting them in bulk to IndexNow. Includes code examples for both beginners and advanced users.
tags:
    - Documentation
    - Tutorial
---

# Sitemap Filter Settings
## Example
When you want full control over which URLs are submitted to IndexNow, the `SitemapFilter` can help. Let's imagine a basic sitemap with three URLs, each with different properties:

```xml linenums="1" title="sitemap.xml" hl_lines="4-5 10-11 16-17"
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

The [date range](date_range.md) filter can ensure that only URLs that has been modified in 2025 are submitted to IndexNow, and furthermore we can exclude any URLs that contain the word `page`. This will effectively submit the URL `https://example.com` to IndexNow because it is the only one that meets these criteria:

```python linenums="1" hl_lines="4-5"
from index_now import DateRange, SitemapFilter, submit_sitemap_to_index_now, IndexNowAuthentication

year_2025 = DateRange(
    start=datetime(2025, 1, 1),
    end=datetime(2025, 12, 31),
)

filter = SitemapFilter(date_range=year_2025, excludes="page")

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

submit_sitemap_to_index_now(
    authentication, "https://example.com/sitemap.xml", filter)
```

## Documentation
### `SitemapFilter`
::: index_now.sitemap.filter.sitemap.SitemapFilter
