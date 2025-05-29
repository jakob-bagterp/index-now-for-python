from datetime import datetime

import pytest

from index_now import (Between, DateRange, DaysAgo, EarlierThan,
                       EarlierThanAndIncluding, LaterThan,
                       LaterThanAndIncluding, Today, Yesterday)


@pytest.mark.parametrize("date_range1, date_range2, expected", [
    (DateRange(start=datetime(2025, 1, 1), end=datetime(2025, 1, 31)), DateRange(start=datetime(2025, 1, 1), end=datetime(2025, 1, 31)), True),
    (DateRange(start=datetime(2025, 1, 1), end=datetime(2025, 1, 31)), DateRange(start=datetime(2025, 1, 1), end=datetime(2025, 1, 30)), False),
    (DateRange(start=datetime(2025, 1, 1), end=datetime(2025, 1, 31)), Today(), False),
    (Today(), Today(), True),
    (Yesterday(), Yesterday(), True),
    (DaysAgo(2), DaysAgo(2), True),
    (DaysAgo(1), DaysAgo(2), False),
    (Between(datetime(2025, 1, 1), datetime(2025, 1, 31)), Between(datetime(2025, 1, 1), datetime(2025, 1, 31)), True),
    (Between(datetime(2025, 1, 1), datetime(2025, 1, 31)), Between(datetime(2025, 1, 1), datetime(2025, 1, 30)), False),
    (Today(), DateRange(start=datetime(2025, 1, 1), end=datetime(2025, 1, 31)), False),
    (Yesterday(), DateRange(start=datetime(2025, 1, 1), end=datetime(2025, 1, 31)), False),
    (DaysAgo(2), DateRange(start=datetime(2025, 1, 1), end=datetime(2025, 1, 31)), False),
    (DaysAgo((datetime.today() - datetime(2025, 1, 1)).days), DateRange(start=datetime(2025, 1, 1), end=datetime(2025, 1, 31)), False),
    (LaterThan(datetime(2025, 1, 1)), DateRange(start=datetime(2025, 1, 1), end=datetime(2025, 1, 31)), False),
    (LaterThanAndIncluding(datetime(2025, 1, 1)), DateRange(start=datetime(2025, 1, 1), end=datetime(2025, 1, 31)), False),
    (EarlierThanAndIncluding(datetime(2025, 1, 1)), DateRange(start=datetime(2025, 1, 1), end=datetime(2025, 1, 31)), False),
    (EarlierThan(datetime(2025, 1, 1)), DateRange(start=datetime(2025, 1, 1), end=datetime(2025, 1, 31)), False),
])
def test_equality_of_date_range_classes(date_range1: DateRange, date_range2: DateRange, expected: bool) -> None:
    assert (date_range1 == date_range2) == expected
