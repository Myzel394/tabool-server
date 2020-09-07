from datetime import datetime, timedelta

from django.test import TestCase

from .models import Event


class ModelTest(TestCase):
    def test_create(self):
        start = datetime.now()
        end = start + timedelta(hours=2)
        
        event = Event.objects.create(
            start_datetime=start,
            end_datetime=end,
            title="Event Test",
            description="Das ist test. Bla oh, ja!"
        )
