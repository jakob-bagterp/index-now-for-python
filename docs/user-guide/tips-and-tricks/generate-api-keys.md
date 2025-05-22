---
title: How to Generate API Keys for IndexNow
description: Learn how to generate API keys to verify your website and submit URLs to IndexNow. Includes code examples for beginners and advanced users.
tags:
    - Tutorial
    - Settings
    - API Key
---

# How to Generate API Keys for IndexNow
## Why Use an API Key?
To use the IndexNow API, you need to set an API key on your website to verify ownership of your domain. This should be kept secret and is required every time you submit a URL to the IndexNow API.

## Requirements
According to the [IndexNow documentation](https://www.indexnow.org/documentation), the requirements are:

!!! quote
    Your-key should have a minimum of 8 and a maximum of 128 hexadecimal characters. The key can contain only the following characters: lowercase characters (a-z), uppercase characters (A-Z), numbers (0-9), and dashes (-).

## Generating Custom API Keys
If you don't want to use the [API key generator from Microsoft Bing](https://www.bing.com/indexnow/getstarted#implementation), you can create your own API key. In this example, we will generate a random 32-character hexadecimal string as an API key:

```python linenums="1"
import uuid

def generate_random_api_key() -> str:
    return str(uuid.uuid4()).replace("-", "")[:32]

print(generate_random_api_key())
```

This will output `5017988d51af458491d21ecab6ed1811` or similar 32-character hexadecimal string.
