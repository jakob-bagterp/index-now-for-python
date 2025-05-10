import pytest
from _mock_data.website import (BROWSERIST, COLORIST_FOR_PYTHON,
                                TIMER_FOR_PYTHON, IndexNowWebsiteData)
from colorist import Color

from index_now import SearchEngineEndpoint, submit_sitemap_to_index_now


@pytest.mark.parametrize("website_data", [
    TIMER_FOR_PYTHON,
    COLORIST_FOR_PYTHON,
    BROWSERIST,
])
def test_submit_sitemap_to_index_now(website_data: IndexNowWebsiteData, capfd: object) -> None:
    submit_sitemap_to_index_now(website_data.authentication, website_data.sitemap_url, endpoint=SearchEngineEndpoint.INDEXNOW)
    terminal_output, _ = capfd.readouterr()
    assert "URL(s) submitted successfully to the IndexNow API:" in terminal_output
    assert f"Status code: {Color.GREEN}200{Color.OFF}" in terminal_output
