import random
from abc import ABC

from django.test import TestCase

from apps.django.main.school_data.models import Room
from apps.django.utils.tests_mixins import joinkwargs

__all__ = [
    "RoomTestMixin"
]


class RoomTestMixin(TestCase, ABC):
    @staticmethod
    def Create_room(**kwargs) -> Room:
        place = ""
        
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
