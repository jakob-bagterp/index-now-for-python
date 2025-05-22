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

## Generating Custom API Keys
If you don't want to use the [API key generator from Microsoft Bing](https://www.bing.com/indexnow/getstarted#implementation), you can create your own API key.

### Requirements
According to the [IndexNow documentation](https://www.indexnow.org/documentation), the requirements are:

!!! quote
    Your-key should have a minimum of 8 and a maximum of 128 hexadecimal characters. The key can contain only the following characters: lowercase characters (a-z), uppercase characters (A-Z), numbers (0-9), and dashes (-).

### Basic Usage
In this example, we will generate a random 32 character hexadecimal string as an API key using the [`generate_api_key()`](../../reference/methods/generate-api-key.md) method:

```python linenums="1" hl_lines="3"
from index_now import generate_api_key

api_key = generate_api_key()

print(api_key)
```

This will output a 32 character hexadecimal string:

```shell title=""
5017988d51af458491d21ecab6ed1811
```

### Custom Length
The [`generate_api_key()`](../../reference/methods/generate-api-key.md) method can also generate API keys of different lengths. Simply adjust the `length` parameter:

```python linenums="1" hl_lines="3-4"
from index_now import generate_api_key

api_key_16 = generate_api_key(length=16)
api_key_64 = generate_api_key(length=64)

print(api_key_16)
print(api_key_64)
```

This will print two random API keys of 16 and 64 characters. Example:

```shell title=""
5017988d51af4584
5017988d51af458491d21ecab6ed18115017988d51af458491d21ecab6ed1811
```
