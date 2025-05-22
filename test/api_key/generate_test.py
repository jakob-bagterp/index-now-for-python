import re

import pytest

from index_now import generate_api_key


def compile_regex_pattern(length: int) -> re.Pattern[str]:
    """Compile a regex pattern for the API key based on the length. Adheres to the IndexNow speficication: https://www.indexnow.org/documentation"""

    return re.compile(r"^[a-zA-Z0-9-]{" + str(length) + "}$")


def test_generate_random_api_key_with_default_length() -> None:
    api_key_pattern = compile_regex_pattern(32)
    for _ in range(100):
        api_key = generate_api_key()
        assert api_key_pattern.match(api_key)


@pytest.mark.parametrize("length", [8, 16, 32, 64, 128])
def test_generate_random_api_key_with_custom_length(length: int) -> None:
    api_key_pattern = compile_regex_pattern(length)
    api_key = generate_api_key(length)
    assert api_key_pattern.match(api_key)
