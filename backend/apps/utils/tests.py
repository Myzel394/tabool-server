from datetime import datetime, time, timedelta
from typing import *

import names
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from apps.utils.time import dummy_datetime_from_time

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
            
            if not Model.objects.all().filter(last_name__iexact=last_name).exists():
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


class StartTimeEndTimeTestMixin(TestCase):
    DURATION = 45
    
    @staticmethod
    def start_time() -> time:
        return datetime.now().time()
    
    @classmethod
    def end_time(cls) -> time:
        return (dummy_datetime_from_time(cls.start_time()) + timedelta(minutes=cls.DURATION)).time()


class ClientTestMixin(TestCase):
    client = Client()
    
    def assertStatusOk(self, status_code: int) -> None:
        self.assertTrue(200 <= status_code <= 299, f"status_code is '{status_code}'")


# TODO: joinkwargs überall hinzufügen!

def joinkwargs(defaults: Dict[str, Callable], given: dict, /) -> dict:
    data = {}
    for key, value in defaults.items():
        if key in given:
            data[key] = given[key]
        else:
            data[key] = value()
            
    return data

