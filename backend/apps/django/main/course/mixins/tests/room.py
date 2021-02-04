import random

from django.test import TestCase

from apps.django.main.course.models import Room
from apps.django.utils.tests_mixins import joinkwargs


class RoomTestMixin(TestCase):
    @staticmethod
    def Create_room(**kwargs) -> Room:
        while True:
            place = str(random.randint(100, 999))
            
            if not Room.objects.filter(place=place).exists():
                break
        
        return Room.objects.create(
            **joinkwargs(
                {
                    "place": lambda: place,
                },
                kwargs
            )
        )
