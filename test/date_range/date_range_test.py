from datetime import datetime, timedelta

import pytest

from index_now import DateRange

JAN_1_2025 = datetime(2025, 1, 1)


@pytest.mark.parametrize("start, end, date_to_check, expected", [
    (datetime.today(), datetime.today(), datetime.today(), True),
    (datetime.now(), datetime.now(), datetime.now(), True),
    (datetime.today() + timedelta(days=1), datetime.today(), datetime.today(), False),  # Tomorrow.
    (datetime.today() - timedelta(days=1), datetime.today(), datetime.today(), True),  # Yesterday.
    (JAN_1_2025, JAN_1_2025, datetime.today(), False),
    (JAN_1_2025, datetime.today(), JAN_1_2025 + timedelta(days=1), True),
    (JAN_1_2025, datetime.today(), JAN_1_2025 - timedelta(days=1), False),
    (JAN_1_2025, datetime.today(), datetime.today() - timedelta(days=1), True),
])
def test_date_range(start: datetime, end: datetime, date_to_check: datetime, expected: bool) -> None:
    date_range = DateRange(start, end)
    assert date_range.is_within_range(date_to_check) == expected
