from datetime import datetime, timedelta

import pytest

from index_now import Yesterday


@pytest.mark.parametrize(
    "date_to_check, expected",
    [
        (datetime.today(), False),
        (datetime.now(), False),
        (datetime.today() + timedelta(days=1), False),  # Tomorrow.
        (datetime.today() - timedelta(days=1), True),  # Yesterday.
        (datetime.today() - timedelta(days=2), False),
        (datetime(2023, 1, 1), False),
    ],
)
def test_date_range_yesterday(date_to_check: datetime, expected: bool) -> None:
    date_range = Yesterday()
    assert date_range.is_within_range(date_to_check) == expected
