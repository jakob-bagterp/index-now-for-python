---
title: How to Automate Sitemap Submission to IndexNow using GitHub Actions
description: If you're using GitHub Actions to deploy your website and want to improve SEO, you can automate the submission of your sitemap to the IndexNow API. Includes code examples for beginners and advanced users.
tags:
    - Tutorial
    - GitHub Actions
---

# Workflow Automation with GitHub Actions
If you're using [GitHub Actions](https://github.com/features/actions) to build and deploy your site, you can automate the process of submitting your sitemap to the IndexNow API. This is particularly useful if you have a large number of pages on your site and want to submit them all at once when you deploy your site.

## How to Automatically Submit a Sitemap to IndexNow
### GitHub Pages
For users of [GitHub Pages](https://pages.github.com), the easiest way to build and deploy your site is to use the existing [`index-now-submit-sitemap-urls-action` workflow](https://github.com/marketplace/actions/index-now-submit-sitemap-urls-action), as it's based on that package. This will also work if you're using [MkDocs](https://www.mkdocs.org) to build your site with GitHub Pages, but will probably work in many other cases as well.

All you need to do is adapt the example below to your needs:

```yaml linenums="1" title=".github/workflows/submit_sitemap_to_index_now.yml"
name: Submit Sitemap to IndexNow

on:
  workflow_run:
    workflows: [pages-build-deployment]
    types: [completed]

jobs:
  submit-sitemap:
    runs-on: ubuntu-latest
    steps:
      - name: Submit sitemap URLs to IndexNow
        uses: jakob-bagterp/index-now-submit-sitemap-urls-action@v1
        with:
          host: example.com
          api_key: ${{ secrets.INDEX_NOW_API_KEY }}
          api_key_location: https://example.com/${{ secrets.INDEX_NOW_API_KEY }}.txt
          sitemap_locations: https://example.com/sitemap.xml
          endpoint: yandex
```

!!! tip
    The [`workflow_run` event](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#workflow_run) is used to trigger the workflow after the GitHub Pages build and deployment is completed. This ensures that the sitemap is submitted only after the latest changes are live.

    ```yaml linenums="3" title=".github/workflows/submit_sitemap_to_index_now.yml"
    on:
      workflow_run:
        workflows: [pages-build-deployment]
        types: [completed]
    ```

!!! abstract "Checklist"
    Before running the workflow, make sure you have done the following:

    - Added the API key `INDEX_NOW_API_KEY` as a [secret to your repository](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions).
    - Uploaded the API key to the location specified in the `api_key_location` parameter.
    - Updated the URL of the sitemap in the `sitemap_location` parameter.
    - Adjusted the `host`, `endpoint`, and other parameters to suit your needs.

### Custom GitHub Actions Workflow
You can customise your workflow even more, though the starting point is the same: Put a YAML workflow file in the `.github/workflows` directory of your repository. We want the workflow to be triggered every time you push to the `master` branch or create a pull request to the `master` branch, and we will then execute the [`submit_sitemap_to_index_now()`](../../reference/methods/submit-sitemap.md) method.

Example of a workflow file:

```yaml linenums="1" title=".github/workflows/submit_sitemap_to_index_now.yml"
name: Submit sitemap to IndexNow

on:
  pull_request:
    branches:
      - master
  push:
    branches:
      - master

jobs:
  submit-sitemap:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - name: Install dependencies
        run: pip install index-now-for-python
      - name: Submit sitemap to IndexNow
        uses: jannekem/run-python-script-action@v1
        with:
          script: |
            from index_now import submit_sitemap_to_index_now, IndexNowAuthentication, SearchEngineEndpoint

            authentication = IndexNowAuthentication(
              host="example.com",
              api_key="${{ secrets.INDEX_NOW_API_KEY }}",
              api_key_location="https://example.com/${{ secrets.INDEX_NOW_API_KEY }}.txt",
            )

            submit_sitemap_to_index_now(authentication, "https://example.com/sitemap.xml", endpoint=SearchEngineEndpoint.YANDEX)
```

## Event-Triggered Workflows
Imagine that the sitemap is submitted before a site deployment is complete. We don't want this to happen, otherwise we won't be using the most up-to-date sitemap.

There are several ways to trigger workflows in GitHub Actions. The most common options in this context are:

- Use [`needs`](https://docs.github.com/en/actions/writing-workflows/about-workflows#creating-dependent-jobs) when having several jobs in the *same workflow file*.
- Use [`workflow_run`](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_run) when you want to trigger jobs in *different workflow files*.

!!! tip
    If you want to update the workflow example above, simple update the trigger to `workflow_run` instead of `pull_request` and `push`.

    ```yaml linenums="3" title=".github/workflows/submit_sitemap_to_index_now.yml"
    on:
      workflow_run:
        workflows: ["Deploy Website"]
        branches: [master]
        types: [completed]
    ```
