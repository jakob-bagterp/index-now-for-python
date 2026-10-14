from http import HTTPStatus

from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.response import BaseHTTPResponse
from urllib3.util.retry import Retry

REQUEST_TIMEOUT_IN_SECONDS = 30

BACKOFF_FACTOR = 1  # Waits 0, 2, 4 seconds between retries.

# Upper limit for the `Retry-After` header, so a long wait doesn't block the submission:
MAX_RETRY_AFTER_IN_SECONDS = 10

RETRY_STATUS_CODES = frozenset(
    {
        HTTPStatus.TOO_MANY_REQUESTS,
        HTTPStatus.INTERNAL_SERVER_ERROR,
        HTTPStatus.BAD_GATEWAY,
        HTTPStatus.SERVICE_UNAVAILABLE,
        HTTPStatus.GATEWAY_TIMEOUT,
    }
)


class CappedRetry(Retry):
    """Retry that respects the `Retry-After` header of `429` and `503` responses, but never waits longer than `MAX_RETRY_AFTER_IN_SECONDS`. Without the limit, an endpoint that responds with e.g. `Retry-After: 3600` would block the submission for an hour instead of letting it fall back to the next endpoint."""

    def get_retry_after(self, response: BaseHTTPResponse) -> float | None:
        retry_after = super().get_retry_after(response)
        if retry_after is None:
            return None
        return min(retry_after, MAX_RETRY_AFTER_IN_SECONDS)


def create_session(retries: int = 0) -> Session:
    """Create a session that retries requests on connection errors, read errors and transient server errors with exponential backoff.

    Submissions to the IndexNow API are idempotent, so it is safe to also retry `POST` requests.

    Args:
        retries (int, optional): Number of retries. Defaults to `0`, i.e. no retries.

    Returns:
        Session: Session with retry logic mounted for both HTTP and HTTPS.

    Raises:
        ValueError: If `retries` is negative.
    """

    if retries < 0:
        raise ValueError(f"The number of retries can't be negative, but was {retries}.")
    retry = CappedRetry(
        total=retries,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=RETRY_STATUS_CODES,
        allowed_methods=frozenset({"GET", "POST"}),
        raise_on_status=False,  # Return the last response when retries are exhausted, so status codes can be handled.
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get(url: str, retries: int = 0, **kwargs: object) -> Response:
    """Send a `GET` request with optional retries and a default timeout."""

    kwargs.setdefault("timeout", REQUEST_TIMEOUT_IN_SECONDS)
    with create_session(retries) as session:
        return session.get(url, **kwargs)  # type: ignore[arg-type]


def post(url: str, retries: int = 0, **kwargs: object) -> Response:
    """Send a `POST` request with optional retries and a default timeout."""

    kwargs.setdefault("timeout", REQUEST_TIMEOUT_IN_SECONDS)
    with create_session(retries) as session:
        return session.post(url, **kwargs)  # type: ignore[arg-type]
