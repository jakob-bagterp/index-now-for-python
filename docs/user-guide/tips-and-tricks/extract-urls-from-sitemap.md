---
title: How to Extract URLs from a Sitemap
description: Learn how to get URLs from an XML sitemap. Includes code examples for beginners and advanced users.
tags:
    - Tutorial
    - Sitemap
---

# How to Extract URLs from a Sitemap
## Using External Libraries
The easiest way to obtain URLs from a sitemap is to parse the sitemap XML file using the [`lxml` library](https://lxml.de). Example:

```python linenums="1"
import requests
import lxml.etree

response = requests.get(https://example.com/sitemap.xml)
sitemap_tree = lxml.etree.fromstring(response.content)
sitemap_urls = sitemap_tree.xpath("//ns:url/ns:loc/text()", namespaces={"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"})

for url in sitemap_urls:
    print(url.strip())
```

This will print all the URLs from the sitemap:

```shell title=""
https://example.com
https://example.com/page1
https://example.com/page2
...
```

## Using Existing Methods
Alternatively, you can simplify the process and use the existing methods in IndexNow for Python to retrieve and parse the sitemap XML file:

```python linenums="1" hl_lines="4-5"
from index_now.sitemap.get import get_sitemap_xml
from index_now.sitemap.parse import parse_sitemap_xml_and_get_urls

sitemap_content = get_sitemap_xml(https://example.com/sitemap.xml)
urls = parse_sitemap_xml_and_get_urls(sitemap_content)

for url in urls:
    print(url)
```

The end result will be the same:

```shell title=""
https://example.com
https://example.com/page1
https://example.com/page2
...
```
