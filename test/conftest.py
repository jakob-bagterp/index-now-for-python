import pytest


@pytest.fixture(autouse=True)
def no_backoff(monkeypatch: pytest.MonkeyPatch) -> None:
    """Disable the backoff between retries, so tests against local endpoints that fail run fast.

    The module is referenced by its import path instead of being imported at the top of this file. Otherwise `index_now` would be imported before pytest collects `src/index_now/conftest.py`, which fails with `ImportPathMismatchError` when the tests run against the installed package (e.g. with tox).
    """

    monkeypatch.setattr("index_now.http_client.BACKOFF_FACTOR", 0)
