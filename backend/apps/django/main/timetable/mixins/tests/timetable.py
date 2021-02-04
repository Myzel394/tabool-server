import random
import string
from datetime import date, timedelta

from django.test import TestCase

from apps.django.main.timetable.models import Timetable
from apps.django.utils.tests_mixins import joinkwargs


class TimetableTestMixin(TestCase):
    @staticmethod
    def Create_timetable(**kwargs) -> Timetable:
        return Timetable.objects.create(
            **joinkwargs({
                "start_date": date.today,
                "end_date": lambda: date.today() + timedelta(days=365),
                "name": lambda: "".join(
                    random.choice(string.ascii_letters)
                    for _ in range(Timetable._meta.get_field("name").max_length)
                )
            }, kwargs)
        )
