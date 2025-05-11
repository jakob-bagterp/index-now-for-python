from pathlib import Path

SITEMAP_FILE_PATH = Path(__file__).parent.parent / "_mock_data" / "sitemap.xml"


def get_mock_sitemap_content() -> str:
    with open(SITEMAP_FILE_PATH) as file:
        content = file.read()
    return content
