from datetime import datetime, timedelta

import pytest

from index_now.sitemap.filter.date_range import DaysAgo


@pytest.mark.parametrize("days_ago, date_to_check, expected", [
    (1, datetime.today(), True),
    (1, datetime.now(), True),
    (1, datetime.today() + timedelta(days=1), False),  # Tomorrow.
    (1, datetime.today() - timedelta(days=1), True),  # Yesterday.
    (1, datetime(2023, 1, 1), False),
    (2, datetime.today(), True),
    (2, datetime.now(), True),
    (2, datetime.today() + timedelta(days=1), False),  # Tomorrow.
    (2, datetime.today() - timedelta(days=1), True),  # Yesterday.
    (2, datetime.today() - timedelta(days=2), True),
    (2, datetime.today() - timedelta(days=3), False),
    (2, datetime(2023, 1, 1), False),
])
def test_date_range_days_ago(days_ago: int, date_to_check: datetime, expected: bool) -> None:
    date_range = DaysAgo(days_ago)
    assert date_range.is_within_range(date_to_check) == expected
