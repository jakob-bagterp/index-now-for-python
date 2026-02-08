from http import HTTPStatus

from index_now.status_code import SUCCESS_STATUS_CODES_COLLECTION_DICTIONARY


def test_status_codes_int_enum() -> None:
    assert HTTPStatus.OK == 200
    assert HTTPStatus.ACCEPTED == 202
    assert HTTPStatus.NO_CONTENT == 204
    assert HTTPStatus.UNPROCESSABLE_ENTITY == 422


def test_status_codes_dict() -> None:
    assert SUCCESS_STATUS_CODES_COLLECTION_DICTIONARY[200] == "OK"
    assert SUCCESS_STATUS_CODES_COLLECTION_DICTIONARY[202] == "Accepted"
    assert SUCCESS_STATUS_CODES_COLLECTION_DICTIONARY[204] == "No Content"
