from dataclasses import dataclass
from enum import Enum, IntEnum, unique


@dataclass(slots=True, frozen=True)
class StatusCode:
    value: int
    response: str

    def __str__(self) -> str:
        return f"{self.value} {self.response}"

    def __repr__(self) -> str:
        return f"{self.value} {self.response}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, StatusCode):
            return self.value == other.value
        else:
            return False

    @property
    def code(self) -> int:
        return self.value


@unique
class StatusCodes(IntEnum):
    OK = 200
    ACCEPTED = 202
    NO_CONTENT = 204
    UNPROCESSABLE_CONTENT = 422


@unique
class StatusCodesCollection(Enum):
    OK = StatusCode(value=StatusCodes.OK, response="OK")
    ACCEPTED = StatusCode(value=StatusCodes.ACCEPTED, response="Accepted")
    NO_CONTENT = StatusCode(value=StatusCodes.NO_CONTENT, response="No content")
    UNPROCESSABLE_CONTENT = StatusCode(value=StatusCodes.UNPROCESSABLE_CONTENT, response="Unprocessable content")

    def __str__(self) -> str:
        return str(self.value.code)

    def __repr__(self) -> str:
        return str(self.value)


SUCCESS_STATUS_CODES = [status_code for status_code in StatusCodes if str(status_code).startswith("2")]

SUCCESS_STATUS_CODES_DICT = {
    status_code.value.code: status_code.value.response
    for status_code in StatusCodesCollection
    if status_code.value.code in SUCCESS_STATUS_CODES
}
