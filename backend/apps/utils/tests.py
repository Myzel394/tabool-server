import random
import string
from contextlib import contextmanager
from datetime import date, datetime, time, timedelta
from typing import *

import names
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from apps.utils.date import find_next_date_by_weekday
from apps.utils.time import dummy_datetime_from_target
from constants import weekdays

__all__ = [
    "UserCreationTestMixin", "StartTimeEndTimeTestMixin", "ClientTestMixin", "joinkwargs"
]


class UserCreationTestMixin(TestCase):
    @staticmethod
    def Create_user(**kwargs) -> settings.AUTH_USER_MODEL:
        Model = get_user_model()
        first_name = names.get_first_name()
        while True:
            last_name = names.get_last_name()
            
            if not Model.objects.filter(last_name__iexact=last_name).exists():
                break
        
        return Model.objects.create_user(
            **{
                "first_name": first_name,
                "last_name": last_name,
                "email": f"{first_name}.{last_name}@gmail.com",
                "password": first_name,
                **kwargs
            }
        )
    
    def Login_user(
            self,
            user: Optional[settings.AUTH_USER_MODEL] = None,
            password: Optional[str] = None
    ) -> settings.AUTH_USER_MODEL:
        """Logs the client in and returns the user with which the client was logged in"""
        self.assertTrue(hasattr(self, "client"), "`client` not available. Add it to the mixins of the test class.")
        
        user = user or self.Create_user()
        
        is_login = self.client.login(
            email=user.email,
            password=password or user.first_name
        )
        
        self.assertTrue(is_login, "Couldn't login the user")
        
        return user
    
    @staticmethod
    def Get_random_password(level: str = "strong") -> str:
        if level == "weak":
            return random.choice(string.ascii_letters + string.digits) * random.choice([2, 5, 12, 20])
        return "".join(
            random.choices(
                string.ascii_letters + string.digits,
                k=random.choice([12, 14, 20, 24])
            )
        )
    
    @contextmanager
    def Login_user_as_context(self, *args, **kwargs):
        previous_value = getattr(self.__class__, "associated_user", None)
        
        try:
            user = self.Login_user(*args, **kwargs)
            self.__class__.associated_user = user
            yield user
        finally:
            self.client.logout()
            self.__class__.associated_user = previous_value


class StartTimeEndTimeTestMixin(TestCase):
    DURATION = 45
    
    @staticmethod
    def start_time() -> time:
        return datetime.now().time()
    
    @classmethod
    def end_time(cls) -> time:
        return (dummy_datetime_from_target(cls.start_time()) + timedelta(minutes=cls.DURATION)).time()


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
