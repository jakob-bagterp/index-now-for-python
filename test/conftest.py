import pytest

from index_now import http_client


@pytest.fixture(autouse=True)
def no_backoff(monkeypatch: pytest.MonkeyPatch) -> None:
    """Disable the backoff between retries, so tests against local endpoints that fail run fast."""

    monkeypatch.setattr(http_client, "BACKOFF_FACTOR", 0)
