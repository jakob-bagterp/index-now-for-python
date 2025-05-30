---
title: How to Submit a URL to IndexNow
description: Learn how to submit a single URL to the IndexNow API to get your page indexed faster by search engines. Includes code examples for beginners and advanced users.
tags:
    - Tutorial
---

# Submit a URL to IndexNow
## How to Submit Individual URLs
If one or more of your website pages have changed and you want each page to be reindexed, you can submit individual URLs to the IndexNow API using the [`submit_url_to_index_now()`](../../reference/methods/submit-single-url.md) method:

```python linenums="1" hl_lines="9 11 13"
from index_now import submit_url_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

submit_url_to_index_now(authentication, "https://example.com/page1")

submit_url_to_index_now(authentication, "https://example.com/page2")

submit_url_to_index_now(authentication, "https://example.com/page3")
```
