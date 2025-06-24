from index_now.status_code import SUCCESS_STATUS_CODES_DICT, StatusCode


def test_status_codes_int_enum() -> None:
    assert StatusCode.OK == 200
    assert StatusCode.ACCEPTED == 202
    assert StatusCode.NO_CONTENT == 204
    assert StatusCode.UNPROCESSABLE_CONTENT == 422


def test_status_codes_dict() -> None:
    assert SUCCESS_STATUS_CODES_DICT[200] == "OK"
    assert SUCCESS_STATUS_CODES_DICT[202] == "Accepted"
    assert SUCCESS_STATUS_CODES_DICT[204] == "No content"
