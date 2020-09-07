from datetime import date, datetime, time
from typing import *

AnyDatetimeModule = Union[date, datetime, time]


def format_datetime(value: AnyDatetimeModule, /, format: Optional[str] = None) -> str:
    default_formats = {
        date: "%d. %m. %Y",
        datetime: "%d. %m. %Y, %H:%M",
        time: "%H:%M"
    }
    format = format or default_formats[type(value)]
    
    return value.strftime(format)


def dummy_datetime_from_time(value: time) -> datetime:
    now = datetime.now()
    
    return datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=value.hour,
        minute=value.minute,
        second=value.second,
        microsecond=value.microsecond
    )
