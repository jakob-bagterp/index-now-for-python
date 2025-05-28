from datetime import datetime, timedelta

import pytest

from index_now import Today


@pytest.mark.parametrize("date_to_check, expected", [
    (datetime.today(), True),
    (datetime.now(), True),
    (datetime.today() + timedelta(days=1), False),  # Tomorrow.
    (datetime.today() - timedelta(days=1), False),  # Yesterday.
    (datetime(2023, 1, 1), False),
])
def test_date_range_today(date_to_check: datetime, expected: bool) -> None:
    date_range = Today()
    assert date_range.is_within_range(date_to_check) == expected
