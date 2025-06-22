[![Latest version](https://img.shields.io/static/v1?label=version&message=1.0.5&color=yellowgreen)](https://github.com/jakob-bagterp/index-now-for-python/releases/latest)
[![Python 3.10 | 3.11 | 3.12 | 3.13+](https://img.shields.io/static/v1?label=python&message=3.10%20|%203.11%20|%203.12%20|%203.13%2B&color=blueviolet)](https://www.python.org)
[![MIT license](https://img.shields.io/static/v1?label=license&message=MIT&color=blue)](https://github.com/jakob-bagterp/index-now-for-python/blob/master/LICENSE.md)
[![Codecov](https://codecov.io/gh/jakob-bagterp/index-now-for-python/branch/master/graph/badge.svg?token=SGVMPJ1JWI)](https://codecov.io/gh/jakob-bagterp/index-now-for-python)
[![CodeQL](https://github.com/jakob-bagterp/index-now-for-python/actions/workflows/codeql.yml/badge.svg)](https://github.com/jakob-bagterp/index-now-for-python/actions/workflows/codeql.yml)
[![Test](https://github.com/jakob-bagterp/index-now-for-python/actions/workflows/test.yml/badge.svg)](https://github.com/jakob-bagterp/index-now-for-python/actions/workflows/test.yml)
[![Downloads](https://static.pepy.tech/badge/index-now-for-python)](https://pepy.tech/project/index-now-for-python)

# 🔍 Submit URLs to the IndexNow API of Various Search Enginges 🔎
Are you concerned about search engine optimization (SEO)? Do you want to make sure your website is indexed frequently by [Bing](https://www.bing.com/indexnow), [Yandex](https://yandex.com/indexnow), [DuckDuckGo](https://duckduckgo.com/), and other search engines?

IndexNow for Python is a lightweight, yet powerful Python package that makes it easy to submit URLs or entire sitemaps to the IndexNow API of various search engines, so your pages can be indexed faster.

Ready to try? Learn [how to install](https://jakob-bagterp.github.io/index-now-for-python/getting-started/installation/) and find tutorials in the [user guide](https://jakob-bagterp.github.io/index-now-for-python/user-guide/).

## Getting Started
### Basic Usage and Submit Individual URLs
Firstly, ensure that you have an [API key for IndexNow](https://jakob-bagterp.github.io/index-now-for-python/user-guide/tips-and-tricks/generate-api-keys/). Hereafter, add your authentication credentials to the `IndexNowAuthentication` class, which will be used throughout the examples. You can now submit individual URLs to the IndexNow API:

```python
from index_now import submit_url_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

submit_url_to_index_now(authentication, "https://example.com/page1")
```

> [!IMPORTANT]
> Instances of `authentication = IndexNowAuthentication(...)` below refer to this section:
>
> ```python
> authentication = IndexNowAuthentication(
>     host="example.com",
>     api_key="a1b2c3d4",
>     api_key_location="https://example.com/a1b2c3d4.txt",
> )
> ```

### Submit Multiple URLs in Bulk
How to submit multiple URLs in bulk to the IndexNow API:

```python
from index_now import submit_urls_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(...)

urls = ["https://example.com/page1", "https://example.com/page2", "https://example.com/page3"]

submit_urls_to_index_now(authentication, urls)
```

### Submit Entire Sitemap
How to submit an entire sitemap to the IndexNow API:

```python
from index_now import submit_sitemap_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(...)

sitemap_location = "https://example.com/sitemap.xml"

submit_sitemap_to_index_now(authentication, sitemap_location)
```

### Submit to Specific Search Engines
How to use the default `SearchEngineEndpoint` options or a custom endpoint:

```python
from index_now import submit_url_to_index_now, IndexNowAuthentication, SearchEngineEndpoint

authentication = IndexNowAuthentication(...)

endpoint_bing = SearchEngineEndpoint.BING
endpoint_custom = "https://example.com/indexnow"

for endpoint in [endpoint_bing, endpoint_custom]:
    submit_url_to_index_now(authentication, "https://example.com/page1", endpoint)
```

## Become a Sponsor 🏅
If you find this project helpful, please consider supporting its development. Your donations will help keep it alive and growing. Every contribution, no matter the size, makes a difference.

[Donate on GitHub Sponsors](https://github.com/sponsors/jakob-bagterp)

Thank you for your support! 🙌

## Contribute
If you have suggestions or changes to the module, feel free to add to the code and create a [pull request](https://github.com/jakob-bagterp/index-now-for-python/pulls).

## Report Bugs
If you encounter any issues, you can [report them as bugs or raise issues](https://github.com/jakob-bagterp/index-now-for-python/issues).
