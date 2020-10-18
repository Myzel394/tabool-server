import os

from django.conf import settings
from django.test import TestCase
from dotenv import load_dotenv

__all__ = [
    "DummyUser"
]


class DummyUser(TestCase):
    def load_dummy_user(self) -> None:
        # Load authentication
        load_dotenv(settings.BASE_DIR / ".." / "scooso_data.env")
        self.username = os.getenv("SCOOSO_USERNAME")
        self.password = os.getenv("SCOOSO_PASSWORD")
