from datetime import datetime, time, timedelta

import names
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase, Client

from apps.utils.time import dummy_datetime_from_time


class UserCreationTestMixin(TestCase):
    @staticmethod
    def create_user() -> User:
        Model = get_user_model()
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        
        return Model.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=f"{first_name}.{last_name}@gmail.com",
            username=last_name.capitalize()
        )


class StartTimeEndTimeTestMixin(TestCase):
    DURATION = 45
    
    @property
    def start_time(self) -> time:
        return datetime.now().time()
    
    @property
    def end_time(self) -> time:
        return (dummy_datetime_from_time(self.start_time) + timedelta(minutes=self.DURATION)).time()


class ClientTestMixin(TestCase):
    client = Client()
