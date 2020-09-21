from datetime import datetime, time, timedelta
from typing import *

import names
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import Client, TestCase

from apps.utils.time import dummy_datetime_from_time


class UserCreationTestMixin(TestCase):
    @staticmethod
    def Create_user() -> User:
        Model = get_user_model()
        first_name = names.get_first_name()
        while True:
            last_name = names.get_last_name()
            
            if not Model.objects.filter(username=last_name.capitalize()).exists():
                break
        
        return Model.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=f"{first_name}.{last_name}@gmail.com",
            username=last_name.capitalize(),
            password=first_name
        )
    
    def Login_user(self, user: Optional[User] = None, password: Optional[str] = None) -> User:
        """Logs the client in and returns the user with which the client was logged in"""
        self.assertTrue(hasattr(self, "client"), "`client` not available. Add it to the mixins of the test class.")
        
        user = user or self.Create_user()
        
        is_login = self.client.login(
            username=user.username,
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
