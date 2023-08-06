from cccalendar import count_months
from datetime import datetime


def test_count_months():
    assert (count_months(datetime(2021, 1, 1), datetime(2021, 1, 1)) == 1)
    assert (count_months(datetime(2021, 1, 1), datetime(2021, 1, 2)) == 1)
    assert (count_months(datetime(2021, 1, 1), datetime(2021, 1, 31)) == 1)

    assert (count_months(datetime(2021, 1, 1), datetime(2021, 2, 1)) == 2)
    assert (count_months(datetime(2021, 1, 31), datetime(2021, 2, 1)) == 2)
    assert (count_months(datetime(2021, 1, 31), datetime(2021, 2, 28)) == 2)

    assert (count_months(datetime(2021, 1, 31), datetime(2022, 1, 1)) == 13)
