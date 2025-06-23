from dataclasses import dataclass
from enum import Enum


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


class StatusCodes(Enum):
    OK = StatusCode(value=200, response="OK")
    ACCEPTED = StatusCode(value=202, response="Accepted")
    UNPROCESSABLE_CONTENT = StatusCode(value=422, response="Unprocessable content")

    def __str__(self) -> str:
        return str(self.value.code)

    def __repr__(self) -> str:
        return str(self.value)


SUCCESS_STATUS_CODES_DICT = {status_code.value.code: status_code.value.response for status_code in StatusCodes if str(status_code.value.code).startswith("2")}

SUCCESS_STATUS_CODES = list(SUCCESS_STATUS_CODES_DICT.keys())
