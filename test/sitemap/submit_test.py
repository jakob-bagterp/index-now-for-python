import pytest
from colorist import Color

from index_now import IndexNowAuthentication, submit_sitemap_to_index_now


@pytest.mark.parametrize("sitemap_url, authentication", [
    ("https://jakob-bagterp.github.io/timer-for-python/sitemap.xml",
     IndexNowAuthentication(
         host="https://jakob-bagterp.github.io/timer-for-python",
         api_key="6d71a14ac15c4c41a0c19e641f659208",
         api_key_location="https://jakob-bagterp.github.io/timer-for-python/assets/index-now/api-key.txt/",
     )),
    ("https://jakob-bagterp.github.io/colorist-for-python/sitemap.xml",
     IndexNowAuthentication(
         host="https://jakob-bagterp.github.io/colorist-for-python",
         api_key="42a119a493b24c8f915bb44ec4c86714",
         api_key_location="https://jakob-bagterp.github.io/colorist-for-python/assets/index-now/api-key.txt/",
     )),
    ("https://jakob-bagterp.github.io/browserist/sitemap.xml",
     IndexNowAuthentication(
         host="https://jakob-bagterp.github.io/browserist",
         api_key="a739958823fa49b1a36350a90c4ed9d9",
         api_key_location="https://jakob-bagterp.github.io/browserist/assets/index-now/api-key.txt/",
     )),
])
def test_submit_sitemap_to_index_now(sitemap_url: str, authentication: IndexNowAuthentication, capfd: object) -> None:
    submit_sitemap_to_index_now(authentication, sitemap_url)
    terminal_output, _ = capfd.readouterr()
    assert "URL(s) submitted successfully to Bing's IndexNow API" in terminal_output
    assert f"Status code: {Color.GREEN}200{Color.OFF}" in terminal_output
