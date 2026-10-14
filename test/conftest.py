import os

import pytest
from pytest import Config, Item, MonkeyPatch

SKIP_LIVE_SUBMISSION_TESTS = "SKIP_LIVE_SUBMISSION_TESTS"


def pytest_configure(config: Config) -> None:
    config.addinivalue_line("markers", "live: submits to the live IndexNow API endpoints")


def pytest_collection_modifyitems(config: Config, items: list[Item]) -> None:
    """Skip tests that submit to the live IndexNow API endpoints if `SKIP_LIVE_SUBMISSION_TESTS` is `true`, so only one CI job submits the same URLs instead of every job in the test matrix."""

    if os.environ.get(SKIP_LIVE_SUBMISSION_TESTS, "").lower() != "true":
        return
    skip_live = pytest.mark.skip(reason=f"Live submissions are skipped as {SKIP_LIVE_SUBMISSION_TESTS} is true.")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)


@pytest.fixture(autouse=True)
def no_backoff(monkeypatch: MonkeyPatch) -> None:
    """Disable the backoff between retries, so tests against local endpoints that fail run fast.

    The module is referenced by its import path instead of being imported at the top of this file. Otherwise `index_now` would be imported before pytest collects `src/index_now/conftest.py`, which fails with `ImportPathMismatchError` when the tests run against the installed package (e.g. with tox).
    """

    monkeypatch.setattr("index_now.utility.http_client.BACKOFF_FACTOR", 0)
