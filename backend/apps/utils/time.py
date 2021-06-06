from datetime import date, datetime, time
from typing import *

from constants import dates

AnyDatetimeModule = Union[date, datetime, time]


def format_datetime(value: AnyDatetimeModule, /, formats: Optional[str] = None) -> str:
    formats = formats or dates.FORMATS
    use_format = str(formats[type(value).__name__])

    return value.strftime(use_format)
