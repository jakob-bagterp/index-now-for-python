from index_now.status_code import SUCCESS_STATUS_CODES_DICT, StatusCodes


def test_status_codes_int_enum() -> None:
    assert StatusCodes.OK == 200
    assert StatusCodes.ACCEPTED == 202
    assert StatusCodes.NO_CONTENT == 204
    assert StatusCodes.UNPROCESSABLE_CONTENT == 422


def test_status_codes_dict() -> None:
    assert SUCCESS_STATUS_CODES_DICT[200] == "OK"
    assert SUCCESS_STATUS_CODES_DICT[202] == "Accepted"
    assert SUCCESS_STATUS_CODES_DICT[204] == "No content"
