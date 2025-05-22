import re

from index_now import generate_api_key


def test_generate_random_api_key() -> None:
    api_key_pattern = re.compile(r"^[0-9a-f]{32}$")
    for _ in range(100):
        api_key = generate_api_key()
        assert api_key_pattern.match(api_key)
