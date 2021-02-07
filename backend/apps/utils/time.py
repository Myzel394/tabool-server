from datetime import date, datetime, time
from typing import *

from constants import dates

AnyDatetimeModule = Union[date, datetime, time]


def format_datetime(value: AnyDatetimeModule, /, formats: Optional[str] = None) -> str:
    formats = formats or dates.FORMATS
    use_format = str(formats[type(value).__name__])
    
    return value.strftime(use_format)


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
