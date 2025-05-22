---
title: Get Started with IndexNow in 2 Easy Steps
description: Quick guide to installing and using IndexNow for Python, so you can submit your first URLs within minutes. Includes code examples for beginners and advanced users.
tags:
    - Tutorial
    - Installation
    - Authentication
    - API Key
    - PyPI
---

# Get Started in 3 Easy Steps 🚀
Ready to try the easy way to submit URLs to the IndexNow API of various search engines? Let's get started:

## 1. Install IndexNow for Python Package
Assuming that [Python](https://www.python.org/) is already installed, execute this command in the terminal to install the Timer package:

```shell title=""
pip install index-now-for-python
```

Find more details and options in the [installation guide](installation.md).

## 2. Set Up an API Key
To verify ownership of your domain, you need to create an API key. This key is hosted on your website so that the IndexNow API service can authenticate your requests. The API key is required each time you submit a URL to the IndexNow API.

For more information about the API key, see the [official IndexNow documentation](https://www.indexnow.org/api-key) or the [getting started guide from Microsoft Bing](https://www.bing.com/indexnow/getstarted#implementation). Or learn [how to generate your own API key](../user-guide/tips-and-tricks/generate-api-keys.md).

## 3. First Script
You're now ready to submit your first URL to the IndexNow API:

```python linenums="1"
from index_now import submit_url_to_index_now, IndexNowAuthentication

authentication = IndexNowAuthentication(
    host="example.com",
    api_key="a1b2c3d4",
    api_key_location="https://example.com/a1b2c3d4.txt",
)

submit_url_to_index_now(authentication, "https://example.com/page1")
```

## Next Steps
Find more usage examples and tutorials in the [user guide](../user-guide/index.md) section.

!!! tip "Become a Sponsor"
    If you find this project helpful, please consider supporting its development. Your donations will help keep it alive and growing. Every contribution, no matter the size, makes a difference.

    [Donate on GitHub Sponsors](https://github.com/sponsors/jakob-bagterp){ .md-button .md-button--primary }

    Thank you for your support! 🙌
