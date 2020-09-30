from datetime import date, timedelta
from typing import *

from .parsers import TimetableParser
from .request import Request
from .. import constants

__all__ = [
    "TimetableRequest"
]


class TimetableRequest(Request):
    def get_timetable(
            self,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None
    ) -> dict:
        start_date = start_date or date.today()
        end_date = end_date or start_date + timedelta(days=5)
        
        return self.request_with_parser(
            url=constants.TIMETABLE_CONNECTION["url"],
            method=constants.TIMETABLE_CONNECTION["method"],
            parser=TimetableParser,
            data={
                "cmd": 600,
                "subcmd": 100,
                "startDate": start_date.strftime(constants.TIMETABLE_CONNECTION["dt_format"]),
                "endDate": end_date.strftime(constants.TIMETABLE_CONNECTION["dt_format"]),
            }
        )
