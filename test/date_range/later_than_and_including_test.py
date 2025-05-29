from datetime import datetime, timedelta

import pytest

from index_now import LaterThanAndIncluding

JAN_1_2025 = datetime(2025, 1, 1)


@pytest.mark.parametrize("date, date_to_check, expected", [
    (datetime.today(), datetime.today(), True),
    (datetime.now(), datetime.now(), True),
    (datetime.today() + timedelta(days=1), datetime.today(), False),  # Tomorrow.
    (datetime.today() - timedelta(days=1), datetime.today(), True),  # Yesterday.
    (JAN_1_2025, datetime.today(), True),
    (JAN_1_2025, JAN_1_2025 + timedelta(days=1), True),
    (JAN_1_2025, JAN_1_2025 - timedelta(days=1), False),
    (JAN_1_2025, datetime.today() - timedelta(days=1), True),
])
def test_date_range_later_than_and_including(date: datetime, date_to_check: datetime, expected: bool) -> None:
    date_range = LaterThanAndIncluding(date)
    assert date_range.is_within_range(date_to_check) == expected
