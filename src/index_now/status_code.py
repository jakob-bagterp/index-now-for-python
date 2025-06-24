from dataclasses import dataclass
from enum import Enum, IntEnum, unique


@dataclass(slots=True, frozen=True)
class StatusCodeSet:
    value: int
    response: str

    @property
    def code(self) -> int:
        return self.value


@unique
class StatusCode(IntEnum):
    OK = 200
    ACCEPTED = 202
    NO_CONTENT = 204
    UNPROCESSABLE_CONTENT = 422


@unique
class StatusCodeCollection(Enum):
    OK = StatusCodeSet(value=StatusCode.OK, response="OK")
    ACCEPTED = StatusCodeSet(value=StatusCode.ACCEPTED, response="Accepted")
    NO_CONTENT = StatusCodeSet(value=StatusCode.NO_CONTENT, response="No content")
    UNPROCESSABLE_CONTENT = StatusCodeSet(value=StatusCode.UNPROCESSABLE_CONTENT, response="Unprocessable content")


SUCCESS_STATUS_CODES = [status_code for status_code in StatusCode if str(status_code).startswith("2")]

SUCCESS_STATUS_CODES_DICT = {
    status_code.value.code: status_code.value.response
    for status_code in StatusCodeCollection
    if status_code.value.code in SUCCESS_STATUS_CODES
}
