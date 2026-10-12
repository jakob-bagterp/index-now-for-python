---
title: How to Fall Back to Other Search Engines with IndexNow
description: Learn how to provide a list of IndexNow API endpoints, so the submission falls back to the next search engine if an endpoint is unavailable or rejects the submission. Includes code examples for beginners and advanced users.
tags:
    - Tutorial
    - Error Handling
    - API Endpoint
---

# Fall Back to Other Search Engines If an Endpoint Fails
Sometimes a search engine endpoint is temporarily unavailable or rejects submissions for a specific site. Instead of a single endpoint, provide a list of endpoints as fallback strategy. The endpoints are tried in order, and the submission stops at the first endpoint that accepts it:

```python linenums="1" hl_lines="9-13 15-16"
from index_now import submit_url_to_index_now, IndexNowAuthentication, SearchEngineEndpoint

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

endpoints_with_fallback = [
    SearchEngineEndpoint.BING,
    SearchEngineEndpoint.YANDEX,
    SearchEngineEndpoint.SEZNAM,
]

submit_url_to_index_now(authentication, "https://example.com/page1",
    endpoint=endpoints_with_fallback)
```

The same applies to `submit_urls_to_index_now`, `submit_sitemap_to_index_now` and `submit_sitemaps_to_index_now`, and the list can also contain [custom endpoints](../search-engines/custom-endpoint.md).

## Fallback Strategy and Submission Sequence
If a submission fails, the next endpoint in the list is tried. The submission stops at the first endpoint that accepts it, and the remaining endpoints are not used.

If the [`retries` parameter](retries-and-timeouts.md) is set, each endpoint is retried before falling back to the next one, in case of temporary errors such as a dropped connection or `503 Service Unavailable`.

The submission falls back to the next endpoint when:

* The endpoint can't be reached, e.g. if the connection is dropped or times out.
* The endpoint responds with a server error, e.g. `500 Internal Server Error` or `503 Service Unavailable`.
* The endpoint responds with `429 Too Many Requests`.
* The endpoint responds with `403 Forbidden`, as some endpoints reject sites that other endpoints accept.

Other client errors, such as `400 Bad Request` or `422 Unprocessable Entity`, indicate a problem with the submission itself, so the submission does not fall back to other endpoints.

If all endpoints fail, the [status code](status-codes.md) of the last response is returned. If none of the endpoints responded at all, the last connection error or timeout is raised instead.

!!! warning
    It is not recommended to submit the same URLs to multiple endpoints. Once you have successfully submitted to one [IndexNow](https://www.indexnow.org) endpoint, the IndexNow service is designed to propagate your URLs to other search engines, so you do not need to submit to multiple times.
