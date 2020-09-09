import random
from abc import ABC

import names
from django.test import TestCase

from apps.timetable.models import Room, Subject, Teacher


class TeacherTestMixin(TestCase, ABC):
    @staticmethod
    def Create_teacher(**kwargs) -> Teacher:
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        
        return Teacher.objects.create(
            **{
                "first_name": first_name,
                "last_name": last_name,
                "email": (
                    f"{first_name}.{last_name}@gmail.com"
                    if random.choice([True, False]) else
                    None
                ),
                **kwargs
            }
        )


class RoomTestMixin(TestCase, ABC):
    @staticmethod
    def Create_room(**kwargs) -> Room:
        return Room.objects.create(
            **{
                "place": f"{random.choice(range(3 + 1))}{random.choice(list(range(99)))}",
                **kwargs
            }
        )


class SubjectTestMixin(TestCase, ABC):
    @staticmethod
    def Create_subject(**kwargs) -> Subject:
        return Subject.objects.create(
            **{
                "name": random.choice([
                    "Mathe",
                    "Englisch",
                    "Deutsch",
                    "Physik",
                    "Biologie",
                    "Chemie",
                    "Geschichte",
                    "Informatik",
                    "Musik",
                    "Kunst",
                    "Sport",
                    "Ethik",
                    "Geschichte"
                ]),
                **kwargs
            }
        )
