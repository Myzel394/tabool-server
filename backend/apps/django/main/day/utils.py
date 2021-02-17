from datetime import date, timedelta

__all__ = [
    "get_date"
]


def get_date() -> date:
    date = date.today()
    weekday = today.weekday()
    
    if weekday >= 5:
        today += timedelta(days=7 - weekday)
    
    return date
