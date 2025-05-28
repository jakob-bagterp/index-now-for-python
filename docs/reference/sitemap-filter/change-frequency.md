---
title: Documentation for Change Frequency Filter Options
description: Learn how to use change frequency options to filter URLs from a sitemap before submitting them in bulk to IndexNow. Includes code examples for both beginners and advanced users.
tags:
    - Documentation
    - Tutorial
---

# Change Frequency Filter Options
## Example
Let's imagine a basic sitemap with three URLs, each with different change frequencies:

```xml linenums="1" title="sitemap.xml" hl_lines="6 12 18"
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

With `ChangeFrequency.DAILY` in the [`SitemapFilter`](sitemap-filter.md) we can target any URLs that have a change frequency of `daily`. Effectively, this will submit the URL `https://example.com/page2` to IndexNow because only it has that change frequency:

```python linenums="1" hl_lines="9"
from index_now import submit_sitemap_to_index_now, IndexNowAuthentication, SitemapFilter, ChangeFrequency

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

filter = SitemapFilter(change_frequency=ChangeFrequency.DAILY)

submit_sitemap_to_index_now(
    authentication, "https://example.com/sitemap.xml", filter)
```

## Documentation
### `ChangeFrequency`
::: index_now.sitemap.filter.change_frequency.ChangeFrequency
