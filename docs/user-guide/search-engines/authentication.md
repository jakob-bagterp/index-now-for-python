---
title: How to Authenticate Your Site
description: Learn how to use the API key and its location to securely submit URLs from your domain to the IndexNow API. Includes code examples for beginners and advanced users.
tags:
    - Tutorial
    - Settings
    - Authentication
---

# How to Authenticate Your Site with IndexNow
## How to Set Up an API Key
You need to create an API key and upload it to your website to verify ownership of your domain. The [guide from Microsoft Bing](https://www.bing.com/indexnow/getstarted#implementation) is a good starting point. Once the API key is hosted on your website, the IndexNow API service can now authenticate your requests.

The API key will be required every time you submit a URL to any IndexNow API.

!!! info "API Key Checklist"
    The example key `a1b2c3d4` won't work, so try the [API key generator from Microsoft Bing](https://www.bing.com/indexnow/getstarted#implementation) instead:

    1. Generate an API key.
    2. Upload a text file containing the API key to your website. This is the API key location.

    Example of a key file:

    ```python title="example.com/a1b2c3d4.txt"
    a1b2c3d4
    ```

    The key file doesn't have to be named `a1b2c3d4.txt` or placed in the root of your website, but this is considered the default location used by IndexNow. As long as the key file contains the API key `a1b2c3d4` and the file location is referenced on every submission, your requests should be accepted:

    ```python title="example.com/my-api-key-location.txt"
    a1b2c3d4
    ```

    If you're in any doubt, you can find more information about API keys in the [official IndexNow documentation](https://www.indexnow.org/api-key).

## How to Use Authentication Credentials
Once you have an API key and secured the location of the API key file, you can now update the [`IndexNowAuthentication`](../../reference/configuration/authentication.md) class with the authentication credentials and submit individual URLs to the IndexNow API:

```python linenums="1" hl_lines="3-7"
from index_now import submit_url_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

submit_url_to_index_now(authentication, "https://example.com/page1")
```

## Use the Same Authentication for Multiple Methods
Whether you submit a single URL, multiple URLs, or an entire sitemap, the authentication credentials remain the same:

```python linenums="1" hl_lines="11 13 15"
from index_now import submit_url_to_index_now, submit_urls_to_index_now, submit_sitemap_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

urls = ["https://example.com/page1", "https://example.com/page2", "https://example.com/page3"]

submit_url_to_index_now(authentication, urls[0])

submit_urls_to_index_now(authentication, urls)

submit_sitemap_to_index_now(authentication, "https://example.com/sitemap.xml")
```

!!! tip
    Because the API key and authentication credentials are required each time you submit URLs to the IndexNow API, it's a good idea to create an IndexNowAuthentication class once and reuse it in all your scripts. Then you won't have to repeat the authentication credentials each time you submit a URL or more.

    For example, how to keep separate files in the same directory:

    ```python title="authentication.py"
    from index_now import IndexNowAuthentication

    my_authentication = IndexNowAuthentication(
        host="example.com",
        api_key="a1b2c3d4",
        api_key_location="https://example.com/a1b2c3d4.txt",
    )
    ```

    ```python title="submit_url.py"
    from index_now import submit_url_to_index_now
    from .authentication import my_authentication

    submit_url_to_index_now(my_authentication, "https://example.com/page1")
    ```

    ```python title="submit_sitemap.py"
    from index_now import submit_sitemap_to_index_now
    from .authentication import my_authentication

    submit_sitemap_to_index_now(my_authentication, "https://example.com/sitemap.xml")
    ```
