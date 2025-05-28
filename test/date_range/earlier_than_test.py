from datetime import datetime, timedelta

import pytest

from index_now import EarlierThan

JAN_1_2025 = datetime(2025, 1, 1)


@pytest.mark.parametrize("date, date_to_check, expected", [
    (datetime.today(), datetime.today(), False),
    (datetime.now(), datetime.now(), False),
    (datetime.today() + timedelta(days=1), datetime.today(), True),  # Tomorrow.
    (datetime.today() - timedelta(days=1), datetime.today(), False),  # Yesterday.
    (JAN_1_2025, datetime.today(), False),
    (JAN_1_2025, JAN_1_2025 + timedelta(days=1), False),
    (JAN_1_2025, JAN_1_2025 - timedelta(days=1), True),
    (JAN_1_2025, datetime.today() - timedelta(days=1), False),
])
def test_date_range_earlier_than(date: datetime, date_to_check: datetime, expected: bool) -> None:
    date_range = EarlierThan(date)
    assert date_range.is_within_range(date_to_check) == expected
