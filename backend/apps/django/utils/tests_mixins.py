import random
from datetime import date, datetime, time, timedelta
from typing import *

from django.test import Client, TestCase

from apps.utils.dates import find_next_date_by_weekday
from apps.utils.time import dummy_datetime_from_target
from constants import weekdays

__all__ = [
    "ClientTestMixin", "joinkwargs", "DateUtilsTestMixin",
]


class DateUtilsTestMixin(TestCase):
    @staticmethod
    def dummy_datetime_from_target(target: Union[date, datetime, time]) -> datetime:
        try:
            return dummy_datetime_from_target(target)
        except ValueError:
            # Just return anything, so the test can pass with any value
            return datetime.now()
    
    @staticmethod
    def Random_future_datetime(
            start_from: Optional[datetime] = None,
            max_days_future: int = 30,
            min_days_future: int = 1
    ) -> datetime:
        return (start_from or datetime.now()) + random.choice([
            timedelta(days=days)
            for days in range(min_days_future, max_days_future + 1)
        ]) + random.choice([
            timedelta(hours=hour)
            for hour in range(0, 24)
        ]) + random.choice([
            timedelta(minutes=minute)
            for minute in range(0, 60)
        ])
    
    @classmethod
    def Random_future_date(
            cls,
            start_from: Optional[date] = None,
            max_days_future: int = 30,
            min_days_future: int = 1
    ) -> date:
        return cls.Random_future_datetime(
            cls.dummy_datetime_from_target(start_from),
            max_days_future,
            min_days_future
        ).date()
    
    @classmethod
    def Random_future_time(
            cls,
            start_from: Optional[time] = None
    ) -> time:
        return cls.Random_future_datetime(
            cls.dummy_datetime_from_target(start_from),
        ).time()
    
    @classmethod
    def Random_allowed_datetime(
            cls,
            start_from: Optional[datetime] = None,
            allowed: Sequence[int] = [x[0] for x in weekdays.ALLOWED_WEEKDAYS],
            *args,
            **kwargs
    ) -> datetime:
        return find_next_date_by_weekday(
            cls.Random_future_datetime(start_from, *args, **kwargs),
            random.choice(allowed)
        )


class ClientTestMixin(TestCase):
    client = Client()
    
    def assertStatusOk(self, status_code: int) -> None:
        self.assertTrue(200 <= status_code <= 299, f"status_code is '{status_code}'")
    
    def assertStatusNotOk(self, status_code: int) -> None:
        self.assertTrue(status_code < 200 or status_code > 299, f"status_code is '{status_code}'")


def joinkwargs(defaults: Dict[str, Callable], given: dict, /) -> dict:
    data = {}
    for key, value in defaults.items():
        if key in given:
            data[key] = given[key]
        else:
            data[key] = value()
    
    remaining_keys = set(given.keys()) - set(defaults.keys())
    
    for key in remaining_keys:
        data[key] = given[key]
    
    return data
