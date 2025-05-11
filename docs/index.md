---
title: The Easy Way to Submit URLs to the IndexNow API
description: IndexNow for Python is a lightweight Python package that makes it easy to submit URLs or entire sitemaps to the IndexNow API of various search engines, so your pages can be indexed faster
tags:
    - Tutorial
---

[![Latest version](https://img.shields.io/static/v1?label=version&message=0.1.0&color=yellowgreen)](https://github.com/jakob-bagterp/index-now-for-python/releases/latest)
[![Python 3.10 | 3.11 | 3.12 | 3.13+](https://img.shields.io/static/v1?label=python&message=3.10%20|%203.11%20|%203.12%20|%203.13%2B&color=blueviolet)](https://www.python.org)
[![MIT license](https://img.shields.io/static/v1?label=license&message=MIT&color=blue)](https://github.com/jakob-bagterp/index-now-for-python/blob/master/LICENSE.md)
[![Codecov](https://codecov.io/gh/jakob-bagterp/index-now-for-python/branch/master/graph/badge.svg?token=SGVMPJ1JWI)](https://codecov.io/gh/jakob-bagterp/index-now-for-python)
[![CodeQL](https://github.com/jakob-bagterp/index-now-for-python/actions/workflows/codeql.yml/badge.svg)](https://github.com/jakob-bagterp/index-now-for-python/actions/workflows/codeql.yml)
[![Test](https://github.com/jakob-bagterp/index-now-for-python/actions/workflows/test.yml/badge.svg)](https://github.com/jakob-bagterp/index-now-for-python/actions/workflows/test.yml)
[![Downloads](https://static.pepy.tech/badge/index-now-for-python)](https://pepy.tech/project/index-now-for-python)

# IndexNow for Python 🔎
## Why Use IndexNow for Python?
If you are concerned about search engine optimization (SEO) and want to make sure your website is indexed frequently by [Bing](https://www.bing.com/indexnow), [Yandex](https://yandex.com/indexnow), and other search engines, then IndexNow for Python may be the right choice for you.

IndexNow for Python is a lightweight Python package that makes it easy to submit URLs or entire sitemaps to the IndexNow API of various search engines, so your pages can be indexed faster.

## How It Works
### Basic Usage and Submit Individual URLs
Firstly, ensure that you have an [API key for IndexNow](https://www.indexnow.org/api-key). Hereafter, add your authentication details to the `IndexNowAuthentication` class, which will be used throughout the examples:

```python linenums="1" hl_lines="3-7"
from index_now import submit_url_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)
```

You can now submit individual URLs to the IndexNow API:

```python linenums="8" hl_lines="1"
submit_url_to_index_now(authentication, "https://example.com/page1")
```

### Submit Multiple URLs in Bulk
How to submit multiple URLs in bulk to the IndexNow API:

```python linenums="1" hl_lines="9-11"
from index_now import submit_urls_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

urls = ["https://example.com/page1", "https://example.com/page2", "https://example.com/page3"]

submit_urls_to_index_now(authentication, urls)
```

### Submit Entire Sitemap
How to submit an entire sitemap to the IndexNow API:

```python linenums="1" hl_lines="9-11"
from index_now import submit_sitemap_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

sitemap_url = "https://example.com/sitemap.xml"

submit_sitemap_to_index_now(authentication, sitemap_url)
```

### Submit to Specific Search Engines
How to use the default `SearchEngineEndpoint` options or a custom endpoint:

```python linenums="1" hl_lines="9-13"
from index_now import submit_url_to_index_now, IndexNowAuthentication, SearchEngineEndpoint

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

endpoint_bing = SearchEngineEndpoint.MICROSOFT_BING
endpoint_custom = "https://example.com/indexnow"

for endpoint in [endpoint_bing, endpoint_custom]:
    submit_url_to_index_now(authentication, "https://example.com/page1", endpoint)
```

## Next Steps
Ready to try? [Let's get started](./getting-started/index.md).

!!! tip "Become a Sponsor"
    If you find this project helpful, please consider supporting its development. Your donations will help keep it alive and growing. Every contribution, no matter the size, makes a difference.

    [Donate on GitHub Sponsors](https://github.com/sponsors/jakob-bagterp){ .md-button .md-button--primary }

    Thank you for your support! 🙌
