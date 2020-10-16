from datetime import date, datetime, timedelta
from typing import *


def find_next_date_by_weekday(start_date: Union[date, datetime], weekday: int) -> Union[date, datetime]:
    assert 0 <= weekday <= 6, "Weekday not valid!"
    
    found_date = start_date
    
    while found_date.weekday() != weekday:
        found_date += timedelta(days=1)
    
    return found_date
