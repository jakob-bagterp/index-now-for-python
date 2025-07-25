from pathlib import Path

SITEMAP_FILE_PATH = Path(__file__).parent.parent / "_mock_data" / "sitemap.xml"
SITEMAP_ONLY_URLS_FILE_PATH = Path(__file__).parent.parent / "_mock_data" / "sitemap_only_urls.xml"
SITEMAP_INCONSISTENT_FILE_PATH = Path(__file__).parent.parent / "_mock_data" / "sitemap_inconsistent.xml"


def get_mock_sitemap_content() -> str:
    with open(SITEMAP_FILE_PATH) as file:
        content = file.read()
    return content


def get_mock_sitemap_only_urls_content() -> str:
    with open(SITEMAP_ONLY_URLS_FILE_PATH) as file:
        content = file.read()
    return content


def get_mock_sitemap_inconsistent_content() -> str:
    with open(SITEMAP_INCONSISTENT_FILE_PATH) as file:
        content = file.read()
    return content


INVALID_SITEMAP_LOCATION = "https://jakob-bagterp.github.io/index-now-for-python/invalid-sitemap.xml"

INVALID_SITEMAP_LOCATIONS = [
    INVALID_SITEMAP_LOCATION,
    INVALID_SITEMAP_LOCATION,
]

NON_EXISTING_SITEMAP_LOCATION = "https://jakob-bagterp.github.io/index-now-for-python/non-existing-sitemap.xml"

NON_EXISTING_SITEMAP_LOCATIONS = [
    NON_EXISTING_SITEMAP_LOCATION,
    NON_EXISTING_SITEMAP_LOCATION,
]
