---
title: Documentation of Endpoint Settings
description: Learn how to use different endpoints for the IndexNow API, so you can submit URLs to various search engines.
tags:
    - Documentation
    - Tutorial
    - Settings
    - Bing
    - Naver
    - Seznam
    - Yandex
    - Yep
---

# Endpoint Settings for Search Engines
## `SearchEngineEndpoint`

::: index_now.endpoint.SearchEngineEndpoint

!!! tip
    The IndexNow organisation maintains a list of currently available search engines that support the IndexNow API. Find it here:

    [indexnow.org/searchengines.json](https://www.indexnow.org/searchengines.json)

!!! warning
    It is not recommended to submit the same URLs to multiple endpoints. Once you have successfully submitted to one [IndexNow](https://www.indexnow.org) endpoint, the IndexNow service is designed to propagate your URLs to other search engines, so you do not need to submit to multiple times.
