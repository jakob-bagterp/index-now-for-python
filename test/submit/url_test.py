from _mock_data.website import TIMER_FOR_PYTHON
from colorist import Color

from index_now import SearchEngineEndpoint, submit_url_to_index_now


def test_submit_url_to_index_now(capfd: object) -> None:
    submit_url_to_index_now(TIMER_FOR_PYTHON.authentication, "https://jakob-bagterp.github.io/timer-for-python/", endpoint=SearchEngineEndpoint.INDEXNOW)
    terminal_output, _ = capfd.readouterr()
    assert f"Status code: {Color.RED}422{Color.OFF}" in terminal_output
