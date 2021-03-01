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
        if os.getenv("GITHUB_WORKFLOW"):
            self.username = "username"
            self.password = "password"
            self.scooso_id = "scooso_id"
        else:
            load_dotenv(settings.BASE_DIR / ".." / "scooso_data.env")
            self.username = os.getenv("SCOOSO_USERNAME")
            self.password = os.getenv("SCOOSO_PASSWORD")
            self.scooso_id = os.getenv("SCOOSO_ID")