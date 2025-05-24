---
title: How to Submit an Entire Sitemap or Multiple Sitemaps to IndexNow
description: Learn how to submit an entire sitemap of multiple URLs to the IndexNow API to get your website indexed faster by search engines. Includes code examples for beginners and advanced users.
tags:
    - Tutorial
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

sitemap_urls = [
    "https://example.com/sitemap1.xml",
    "https://example.com/sitemap2.xml",
    "https://example.com/sitemap3.xml",
]

submit_sitemaps_to_index_now(authentication, sitemap_urls)
```

## How to Filter the URLs
Sometimes you want to submit only a subset of the URLs in a sitemap. You can use the `contains`, `skip`, and `take` parameters to filter the URLs before submitting them to the IndexNow API.

For example:

```python linenums="1" hl_lines="9-10"
from index_now import submit_sitemap_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

submit_sitemap_to_index_now(authentication, "https://example.com/sitemap.xml",
    contains="section1", skip=2, take=3)
```

The same applies to submitting multiple sitemaps:

```python linenums="15" hl_lines="1-2"
submit_sitemaps_to_index_now(authentication, sitemap_urls,
    contains="section1", skip=2, take=3)
```

### By Text
You can limit the sitemap URLs to only those containing a specific text using the `contains` parameter:

```python linenums="9" hl_lines="1-2" title=""
submit_sitemap_to_index_now(authentication, "https://example.com/sitemap.xml",
    contains="section1")
```

Example for multiple sitemaps:

```python linenums="15" hl_lines="1-2"
submit_sitemaps_to_index_now(authentication, sitemap_urls,
    contains="section1")
```

#### Use Pattern or Regular Expression
The `contains` parameter also accepts regular expressions for more advanced filtering. For example, if you want to match URLs that contain either `section1` or `section2`, you can use the regular expression `r"(section1)|(section2)"`:

```python linenums="9" hl_lines="1-2" title=""
submit_sitemap_to_index_now(authentication, "https://example.com/sitemap.xml",
    contains=r"(section1)|(section2)")
```

Example for multiple sitemaps:

```python linenums="15" hl_lines="1-2"
submit_sitemaps_to_index_now(authentication, sitemap_urls,
    contains=r"(section1)|(section2)")
```

### By Amount: Skip and Take
Let's imagine a sitemap with a 100 URLs. You don't want to submit everything, so you can use the `skip` and `take` parameters to skip the first 10 URLs and submit the next 20 URLs:

```python linenums="9" hl_lines="1-2" title=""
submit_sitemap_to_index_now(authentication, "https://example.com/sitemap.xml",
    skip=10, take=20)
```

Example for multiple sitemaps:

```python linenums="15" hl_lines="1-2"
submit_sitemaps_to_index_now(authentication, sitemap_urls,
    skip=10, take=20)
```

### Order of Filtering Rules
!!! tip
    When using multiple filtering options at the same time, be aware of the order of the filtering rules. You don't have to use every rule, but each rule can reduce the pool of URLs before passing them on to the next filter.

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
