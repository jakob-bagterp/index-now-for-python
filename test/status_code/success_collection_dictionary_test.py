from http import HTTPStatus

import pytest

from index_now.status_code import SUCCESS_STATUS_CODES_COLLECTION_DICTIONARY


@pytest.mark.parametrize(
    "status_code, expected",
    [
        (HTTPStatus.OK, "OK"),
        (200, "OK"),
        (HTTPStatus.ACCEPTED, "Accepted"),
        (202, "Accepted"),
        (HTTPStatus.NO_CONTENT, "No Content"),
        (204, "No Content"),
    ],
)
def test_status_code_dictionary(status_code: int, expected: str) -> None:
    assert SUCCESS_STATUS_CODES_COLLECTION_DICTIONARY[status_code] == expected
