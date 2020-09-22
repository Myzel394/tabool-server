from datetime import date, timedelta

__all__ = [
    "find_next_date_with_weekday"
]


def find_next_date_with_weekday(start_date: date, weekday: int) -> date:
    assert 0 <= weekday <= 6, "Weekday not valid!"
    
    found_date = start_date
    
    while found_date.weekday() != weekday:
        found_date += timedelta(days=1)
    
    return found_date
