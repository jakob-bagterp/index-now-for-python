---
title: How to Submit URLs to Various Search Engines
description: Learn how to use different endpoints for the IndexNow API, so you can submit URLs to various search engines. Includes code examples for beginners and advanced users.
tags:
    - Tutorial
    - Settings
    - Bing
    - Naver
    - Seznam
    - Yandex
    - Yep
---

# How to Use the Different Search Engine Endpoints
You should not need to use multiple endpoints when using IndexNow. The service is designed to propagate URLs to other search engines once you've submitted successfully to one IndexNow endpoint. But sometimes it's useful to know how to submit to a specific search engine. This guide will show you how to do this.

## Examples
### Basic Usage
The `SearchEngineEndpoint` class contains a list of default search engine endpoints. You can use the same credentials to submit URLs to different IndexNow APIs:

```python linenums="1" hl_lines="9-10 12-13"
from index_now import submit_url_to_index_now, IndexNowAuthentication, SearchEngineEndpoint

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

submit_url_to_index_now(authentication, "https://example.com/page1",
    SearchEngineEndpoint.MICROSOFT_BING)

submit_url_to_index_now(authentication, "https://example.com/page2",
    SearchEngineEndpoint.YANDEX)
```

### Submit to Multiple Endpoints
If you want to submit to multiple search engine endpoints, here's how:

```python linenums="1" hl_lines="9-11"
from index_now import submit_url_to_index_now, IndexNowAuthentication, SearchEngineEndpoint

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

for endpoint in SearchEngineEndpoint:
    submit_url_to_index_now(authentication, "https://example.com/page1",
        endpoint)
```

## List of Default Endpoints
The following endpoints are provided by default with the IndexNow for Python package. If you can't find the endpoint you are looking for, you can also use a [custom endpoint] (custom-endpoint.md).

| Endpoint Enum                         | Name                                           | Endpoint URL                                                                         |
| ------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------ |
| `SearchEngineEndpoint.INDEXNOW`       | [IndexNow](https://www.indexnow.org) (default) | [https://api.indexnow.org/indexnow](https://api.indexnow.org/indexnow)               |
| `SearchEngineEndpoint.MICROSOFT_BING` | [Microsoft Bing](https://www.bing.com)         | [https://www.bing.com/indexnow](https://www.bing.com/indexnow)                       |
| `SearchEngineEndpoint.NAVER`          | [Naver](https://www.naver.com)                 | [https://searchadvisor.naver.com/indexnow](https://searchadvisor.naver.com/indexnow) |
| `SearchEngineEndpoint.SEZNAM`         | [Seznam.cz](https://www.seznam.cz)             | [https://search.seznam.cz/indexnow](https://search.seznam.cz/indexnow)               |
| `SearchEngineEndpoint.YANDEX`         | [Yandex](https://yandex.com)                   | [https://yandex.com/indexnow](https://yandex.com/indexnow)                           |
| `SearchEngineEndpoint.YEP`            | [Yep](https://yep.com)                         | [https://indexnow.yep.com/indexnow](https://indexnow.yep.com/indexnow)               |

!!! tip
    The IndexNow organisation maintains a list of currently available search engines that support the IndexNow API. Find it here:

    [indexnow.org/searchengines.json](https://www.indexnow.org/searchengines.json)
