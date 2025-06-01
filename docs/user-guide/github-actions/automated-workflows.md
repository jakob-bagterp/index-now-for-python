---
title: How to Automate Sitemap Submission to IndexNow using GitHub Actions
description: If you're using GitHub Actions to deploy your website and want to improve SEO, you can automate the submission of your sitemap to the IndexNow API. Includes code examples for beginners and advanced users.
tags:
    - Tutorial
    - GitHub Actions
    - Automation
---

# How to Automatically Submit a Sitemap to IndexNow
If you use [GitHub Actions](https://github.com/features/actions) to build and deploy your website, you can automate the process of submitting your sitemap to the IndexNow API. This is particularly useful if you have a large number of pages on your site that you want to submit all at once.

Find a simplified version of IndexNow for Python on GitHub Actions and begin automating your workflows:

[View on GitHub Marketplace](https://github.com/marketplace/actions/index-now-submit-sitemap-urls-action){ .md-button .md-button--primary }

## Workflow Automation with GitHub Actions
Regardless of whether your codebase is highly or less active, it is recommended that you do _not_ submit your sitemap to IndexNow each time your site is deployed to production. This could overwhelm IndexNow and reduce the website's ranking.

Instead, you should automate sitemap submissions to IndexNow using GitHub Actions at regular intervals, allowing the changes to accumulate over time and allowing the search engines crawlers time to index the latest content.

Example workflow with GitHub Actions:

```yaml linenums="1" title=".github/workflows/submit_sitemap_to_index_now.yml"
name: Submit Sitemap to IndexNow

on:
  schedule:
    - cron: 0 0 1 * *  # Run at midnight UTC on the 1st day of each month.

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
          endpoint: yandex
          sitemap_locations: https://example.com/sitemap.xml
```

!!! abstract "Checklist"
    Before running the workflow, make sure you have done the following:

    - Added the API key `INDEX_NOW_API_KEY` as a [secret to your repository](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions).
    - Uploaded the API key to the location specified in the `api_key_location` parameter.
    - Updated the URL of the sitemap in the `sitemap_location` parameter.
    - Adjusted the `host`, `endpoint`, and other parameters to suit your needs.

## Scheduled Runs
The example above can be adjusted to run at different intervals. Simply adjust the [`cron` job](https://en.wikipedia.org/wiki/Cron) definition to your needs.

!!! warning
    Too many submissions to any of the [IndexNow API endpoints](../search-engines/default-endpoints.md) could result in your site being ranked lower by search engines, maybe even blacklisted. It's highly recommended to only submit sitemaps to the IndexNow API once a day or less, ideally only the latest updated URLs.

### Monthly Schedule
Run the workflow at midnight UTC on the first day of each month:

```yaml linenums="5" title=".github/workflows/submit_sitemap_to_index_now.yml"
    - cron: 0 0 1 * *
```

### Weekly Schedule
Run the workflow at midnight UTC on the first day of each week:

```yaml linenums="5" title=".github/workflows/submit_sitemap_to_index_now.yml"
    - cron: 0 0 * * 0
```

### Daily Schedule
Run the workflow at midnight UTC on a daily basis:

```yaml linenums="5" title=".github/workflows/submit_sitemap_to_index_now.yml"
    - cron: 0 0 * * *
```

#### Only Submit Latest Changes
Rather than submitting all the URLs in the sitemap as one large payload to IndexNow, you can also submit only the latest changes by targeting the latest modification date of each URL in the sitemap using the `<lastmod>` tag. This is particularly useful if you have a large number of pages on your site that you want to submit all at once when deploying your site.

Simply adjust the `sitemap_days_ago` parameter to the desired number of days, as highlighted below:

```yaml linenums="1" title=".github/workflows/submit_sitemap_to_index_now.yml" hl_lines="19"
name: Submit Sitemap to IndexNow

on:
  schedule:
    - cron: 0 0 * * *  # Run daily at midnight UTC.

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
          endpoint: yandex
          sitemap_locations: https://example.com/sitemap.xml
          sitemap_days_ago: 1
```


## Event-Triggered Workflows
Imagine the sitemap is submitted before the site has been fully deployed. This is something we want to avoid, as otherwise we won't be using the most up-to-date sitemap.

There are several ways to trigger workflows in GitHub Actions. The most common options in this context are:

- Use [`needs`](https://docs.github.com/en/actions/writing-workflows/about-workflows#creating-dependent-jobs) when having several jobs in the *same workflow file*.
- Use [`workflow_run`](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_run) when you want to trigger jobs in *different workflow files*.

!!! tip
    If you want to update the previous workflow example, simple update the trigger to `workflow_run` instead of `schedule` and adapt the workflow names to your needs:

    ```yaml linenums="3" title=".github/workflows/submit_sitemap_to_index_now.yml"
    on:
      workflow_run:
        workflows: ["My Deployment Workflow"]
        branches: [master]
        types: [completed]
    ```

### GitHub Pages
For users of [GitHub Pages](https://pages.github.com), you can still use the automated [`index-now-submit-sitemap-urls-action`](https://github.com/marketplace/actions/index-now-submit-sitemap-urls-action) workflow. This will also work if you're using [MkDocs](https://www.mkdocs.org) to build your site with GitHub Pages, and it will probably work in many other cases as well.

All you need to do is adjust the `on` condition and adapt the example below to your needs:

```yaml linenums="3" title=".github/workflows/submit_sitemap_to_index_now.yml"
on:
  workflow_run:
    workflows: [pages-build-deployment]
    types: [completed]
```

!!! info
    The [`workflow_run`](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#workflow_run) event is used to trigger the workflow after the GitHub Pages build and deployment is completed. This ensures that the sitemap is submitted only after the latest changes are live.

## Custom GitHub Actions Workflow
You can customise your workflow even more, although the starting point is the same: Put a YAML workflow file in the `.github/workflows` directory of your repository.

Imagine that we want the workflow to be triggered every time you push to the `master` branch or create a pull request to the `master` branch, and we will then execute the [`submit_sitemap_to_index_now()`](../../reference/methods/submit-sitemap.md) method.

Example of a workflow file:

```yaml linenums="1" title=".github/workflows/custom_workflow.yml"
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

            submit_sitemap_to_index_now(authentication,
                "https://example.com/sitemap.xml", endpoint=SearchEngineEndpoint.YANDEX)
```
