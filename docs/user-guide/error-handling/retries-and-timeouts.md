---
title: How to Retry Failed Submissions to IndexNow
description: Learn how to retry submissions to the IndexNow API automatically in case of temporary errors, such as dropped connections or server errors. Includes code examples for beginners and advanced users.
tags:
    - Tutorial
    - Error Handling
    - Status Codes
---

# Retries and Timeouts
Search engine endpoints are sometimes briefly unavailable, e.g. if the connection is dropped or the server is overloaded. To handle such temporary errors, use the `retries` parameter to retry failed requests automatically before a status code is returned:

```python linenums="1" hl_lines="10"
from index_now import submit_url_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

submit_url_to_index_now(authentication, "https://example.com/page1",
    retries=3)
```

The `retries` parameter is available for all submission methods. By default, it's set to `0`, which means that requests are not retried. When enabled, the following situations are handled:

| Situation                                                      | Behaviour                                                             |
| -------------------------------------------------------------- | --------------------------------------------------------------------- |
| Connection dropped or timed out                                | Retried.                                                              |
| `429 Too Many Requests`                                        | Retried.                                                              |
| `500`, `502`, `503` or `504` server errors                     | Retried.                                                              |
| Other client errors, e.g. `400 Bad Request` or `403 Forbidden` | Not retried, as sending the same request again gives the same result. |

Between retries, the wait time increases exponentially (0, 2, 4 seconds, etc.). If the endpoint responds with a `Retry-After` header, the wait time is respected, but limited to 10 seconds, so a long wait doesn't block the submission.

Regardless of retries, each request has a timeout of 30 seconds, so a request never hangs indefinitely.

When all retries are used, the [status code](status-codes.md) of the last response is returned. If the endpoint didn't respond at all, the last connection error or timeout is raised instead.

!!! tip
    Retries handle temporary errors of a single endpoint. If an endpoint is unavailable for a longer period, you can provide a [list of endpoints as fallback](fallback-strategy.md), so the submission continues with the next endpoint.
