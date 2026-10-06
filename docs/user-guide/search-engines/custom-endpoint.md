---
title: How to Submit URLs to a Custom Endpoint
description: Learn how to submit URLs to a customs endpoint for the IndexNow API. Includes code examples for beginners and advanced users.
tags:
    - Tutorial
    - IndexNow
    - Settings
    - API Endpoint
---

# Custom Search Engine Endpoints for IndexNow
## How to Submit URLs to a Specific Endpoint
If you're not covered by the [default endpoints](default-endpoints.md), you can submit to a custom endpoint. This is useful if you want to submit to a specific search engine or if you have a custom IndexNow endpoint.

```python linenums="1" hl_lines="9-13"
from index_now import submit_url_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

endpoint_custom = "https://example.com/indexnow"

submit_url_to_index_now(authentication, "https://example.com/page1",
    endpoint_custom)
```

## More Information
If you don't know the endpoint URL for a particular search engine, some of the [default endpoints](default-endpoints.md) might be a good place to start.

!!! tip
    The IndexNow organisation maintains a list of currently available search engines that support the IndexNow API. Find it here:

    [indexnow.org/searchengines.json](https://www.indexnow.org/searchengines.json)
