from datetime import date, datetime, time, timedelta
from typing import *

__all__ = [
    "find_next_date_by_weekday", "is_all_day"
]


def find_next_date_by_weekday(start_date: Union[date, datetime], weekday: int) -> Union[date, datetime]:
    assert 0 <= weekday <= 6, "Weekday not valid!"
    
    found_date = start_date
    
    while found_date.weekday() != weekday:
        found_date += timedelta(days=1)
    
    return found_date


def is_all_day(first_datetime: datetime, end_datetime: datetime) -> bool:
    is_full_range = first_datetime == datetime.combine(first_datetime.date(), time.min) \
                    and end_datetime == datetime.combine(end_datetime.date(), time.max)
    is_next_date = (first_datetime + timedelta(days=1)) == end_datetime and first_datetime.time() == time.min
    is_same_date_zero = first_datetime.time() == time.min and end_datetime.time() == time.min
    
    return is_full_range or is_next_date or is_same_date_zero
