from collections.abc import Callable, Sequence
from http import HTTPStatus

import requests
from colorist import Color
from requests.exceptions import ConnectionError, Timeout

from .endpoint import SearchEngineEndpoint
from .status_code import SUCCESS_STATUS_CODES_COLLECTION, SUCCESS_STATUS_CODES_COLLECTION_DICTIONARY

FALLBACK_STATUS_CODES = frozenset({HTTPStatus.FORBIDDEN, HTTPStatus.TOO_MANY_REQUESTS})


def is_fallback_status_code(status_code: int) -> bool:
    """Check whether a failed submission should be tried again at the next endpoint.

    Server errors and rate limits indicate that the endpoint is unavailable, and `403 Forbidden` is endpoint-specific (e.g. some endpoints reject sites that other endpoints accept). Other client errors, such as `400 Bad Request` or `422 Unprocessable Entity`, indicate a problem with the payload that another endpoint will not solve.

    Args:
        status_code (int): Status code of the response.

    Returns:
        bool: `True` if the submission should fall back to the next endpoint, otherwise `False`.
    """

    return status_code in FALLBACK_STATUS_CODES or status_code >= HTTPStatus.INTERNAL_SERVER_ERROR


def submit_with_fallback(
    endpoint: SearchEngineEndpoint | str | Sequence[SearchEngineEndpoint | str],
    send: Callable[[str], requests.Response],
    success_message: str,
    failure_message: str,
) -> int:
    """Submit to one or more endpoints in order and stop at the first success.

    If a list or tuple of endpoints is given, the submission falls back to the next endpoint on connection errors, server errors, `429 Too Many Requests` and `403 Forbidden`.

    Args:
        endpoint (SearchEngineEndpoint | str | Sequence[SearchEngineEndpoint | str]): Endpoint or list of endpoints to try in order.
        send (Callable[[str], requests.Response]): Function that sends the submission to the given endpoint URL.
        success_message (str): Message printed with the endpoint that accepted the submission.
        failure_message (str): Message printed with the endpoint that rejected the submission.

    Returns:
        int: Status code of the first successful response, or of the last response if all endpoints fail.

    Raises:
        ValueError: If an empty list of endpoints is given.
        ConnectionError | Timeout: If no endpoint produced a response.
    """

    endpoints = (
        [str(endpoint)] if isinstance(endpoint, (str, SearchEngineEndpoint)) else [str(item) for item in endpoint]
    )
    if not endpoints:
        raise ValueError("At least one endpoint is required.")
    has_fallback = len(endpoints) > 1

    last_response: requests.Response | None = None
    for index, current_endpoint in enumerate(endpoints):
        is_last_endpoint = index == len(endpoints) - 1
        try:
            response = send(current_endpoint)
        except (ConnectionError, Timeout) as error:
            if not has_fallback:
                raise
            print(
                f"{Color.YELLOW}Failure. Could not connect to this IndexNow API endpoint:{Color.OFF} {current_endpoint}"
            )
            print(f"Error: {Color.RED}{error}{Color.OFF}")
            if is_last_endpoint and last_response is None:
                raise
        else:
            if response.status_code in SUCCESS_STATUS_CODES_COLLECTION:
                print(f"{Color.GREEN}{success_message}{Color.OFF} {current_endpoint}")
                print(
                    f"Status code: {Color.GREEN}{response.status_code} {SUCCESS_STATUS_CODES_COLLECTION_DICTIONARY[response.status_code]}{Color.OFF}"
                )
                return response.status_code
            print(f"{Color.YELLOW}{failure_message}{Color.OFF} {current_endpoint}")
            print(f"Status code: {Color.RED}{response.status_code}{Color.OFF}")
            print(f"Response: {response.text}")
            if not is_fallback_status_code(response.status_code):
                return response.status_code
            last_response = response
        if not is_last_endpoint:
            print(f"Falling back to the next IndexNow API endpoint: {endpoints[index + 1]}")

    # Unreachable, as the last connection error is re-raised above if no endpoint responded:
    if last_response is None:  # pragma: no cover
        raise RuntimeError("No response from any IndexNow API endpoint.")
    if has_fallback:
        print(
            f"{Color.YELLOW}Failure. None of the {len(endpoints)} IndexNow API endpoints accepted the submission.{Color.OFF}"
        )
    return last_response.status_code
