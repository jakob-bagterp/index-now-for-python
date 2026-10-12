from index_now import SitemapFilter

NUMBER_OF_URLS_IN_LIVE_SUBMISSIONS = (
    3  # Enough to test a real submission without resubmitting the whole sitemap on every test run.
)

LIVE_SUBMISSION_SITEMAP_FILTER = SitemapFilter(take=NUMBER_OF_URLS_IN_LIVE_SUBMISSIONS)
