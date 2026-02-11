from http import HTTPStatus

SUCCESS_STATUS_CODES_COLLECTION = {HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT}

SUCCESS_STATUS_CODES_COLLECTION_DICTIONARY = {
    status_code.value: status_code.phrase for status_code in SUCCESS_STATUS_CODES_COLLECTION
}
