from datetime import datetime, timedelta

import pytest

from index_now import Day


@pytest.mark.parametrize("day, date_to_check, expected", [
    (datetime.today(), datetime.today(), True),
    (datetime.now(), datetime.now(), True),
    (datetime.today() + timedelta(days=1), datetime.today(), False),
    (datetime.today() - timedelta(days=1), datetime.today(), False),
    (datetime(2023, 1, 1), datetime.today(), False),
])
def test_date_range_today(day: datetime, date_to_check: datetime, expected: bool) -> None:
    date_range = Day(day)
    assert date_range.is_within_range(date_to_check) == expected
