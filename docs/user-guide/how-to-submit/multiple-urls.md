---
title: How to Submit Multiple URLs to IndexNow
description: Learn how to submit multiple URLs in bulk to the IndexNow API to get your website indexed faster by search engines. Includes code examples for beginners and advanced users.
tags:
    - Tutorial
---

# Submit Multiple URLs to IndexNow
## How to Submit URLs in Bulk
If several pages on your site have changed and you want them all to be reindexed, you can submit a list of URLs in bulk to the IndexNow API using the [`submit_urls_to_index_now()`](../../reference/methods/submit-multiple-urls.md) method:

```python linenums="1" hl_lines="9-15"
from index_now import submit_urls_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
]

submit_urls_to_index_now(authentication, urls)
```
