from datetime import datetime, timedelta

import pytest

from index_now.sitemap.filter.date_range import Day


@pytest.mark.parametrize("date_input, date_to_check, expected", [
    (datetime.today(), datetime.today(), True),
    (datetime.now(), datetime.now(), True),
    (datetime.today() + timedelta(days=1), datetime.today(), False),
    (datetime.today() - timedelta(days=1), datetime.today(), False),
    (datetime(2023, 1, 1), datetime.today(), False),
])
def test_date_range_today(date_input: datetime, date_to_check: datetime, expected: bool) -> None:
    date_range = Day(date_input)
    assert date_range.is_within_range(date_to_check) == expected
