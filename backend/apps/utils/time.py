from datetime import date, datetime, time
from typing import *

AnyDatetimeModule = Union[date, datetime, time]


def format_datetime(value: AnyDatetimeModule, /, format: Optional[str] = None) -> str:
    # TODO: ADd as constants!
    default_formats = {
        date: "%d.%m.%Y",
        datetime: "%d.%m.%Y, %H:%M",
        time: "%H:%M"
    }
    format = format or default_formats[type(value)]
    
    return value.strftime(format)


def dummy_datetime_from_target(target: Union[date, datetime, time]) -> datetime:
    NOW = datetime.now()
    
    if type(target) is datetime:
        return target
    elif type(target) is date:
        return datetime(
            year=target.year,
            month=target.month,
            day=target.day,
            hour=NOW.hour,
            minute=NOW.minute,
            second=NOW.second
        )
    elif type(target) is time:
        return datetime(
            year=NOW.year,
            month=NOW.month,
            day=NOW.day,
            hour=target.hour,
            minute=target.minute,
            second=target.second,
            microsecond=target.minute,
        )
    
    raise ValueError("Date couldn't be converted.")
