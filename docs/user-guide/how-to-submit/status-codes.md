---
title: How to Handle Status Codes from IndexNow
description: Learn how to use the status codes returned from the IndexNow API to determine if URLs were submitted successfully. Includes code examples for beginners and advanced users.
tags:
    - Tutorial
    - Status Codes
---

# How to Use Returned Status Codes
All submission methods return the status code of the response, e.g. `200` for success, `202` for accepted, `400` for bad request, etc.

This can be useful if you want to know if the URLs or sitemaps were submitted successfully to the IndexNow API.

## Example of Status Code as Condition
Before submitting all URLs, you can test if the first URL was submitted successfully and herafter continue with the rest of the URLs. A variation of previous examples:

```python linenums="1" hl_lines="9 12"
from index_now import submit_url_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

status_code = submit_url_to_index_now(authentication,
    "https://example.com/page1")

if status_code in [200, 202]:
    print("URL was submitted successfully to IndexNow.")
    print("Continuing with the rest of the URLs...")

    submit_url_to_index_now(authentication,
        "https://example.com/page2")
    submit_url_to_index_now(authentication,
        "https://example.com/page3")
else:
    print(f"Failure. No URL was submitted to IndexNow. Status code: {status_code}")
```

## Overview of Status Codes
According to the [IndexNow API documentation](https://www.indexnow.org/documentation), the following status codes are returned:

!!! info "Typical Status Codes"
    | Code  | Response             | Description                                                                                           |
    | ----- | -------------------- | ----------------------------------------------------------------------------------------------------- |
    | `200` | OK                   | URL submitted successfully.                                                                           |
    | `202` | Accepted             | URL received. IndexNow key validation pending.                                                        |
    | `400` | Bad request          | The request was invalid.                                                                              |
    | `403` | Forbidden            | In case of key not valid (e.g. key not found, file found but key not in the file).                    |
    | `422` | Unprocessable entity | In case of URLs which don’t belong to the host or the key is not matching the schema in the protocol. |
    | `429` | Too many requests    | Too many requests (potential spam).                                                                   |

    If you get `500` or similar as status code, it's likely that the server is experiencing an error. Then try again later.
