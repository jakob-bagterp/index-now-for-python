from http import HTTPStatus

import pytest


@pytest.mark.parametrize("status_code, expected", [
    (HTTPStatus.OK, 200),
    (HTTPStatus.ACCEPTED, 202),
    (HTTPStatus.NO_CONTENT, 204),
    (HTTPStatus.UNPROCESSABLE_ENTITY, 422),
])
def test_status_code_value(status_code: HTTPStatus, expected: int) -> None:
    assert status_code.value == expected
