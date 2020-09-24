import random
from abc import ABC

from django.test import TestCase

from apps.utils.tests import joinkwargs
from ...models import Room

__all__ = [
    "RoomTestMixin"
]


class RoomTestMixin(TestCase, ABC):
    @staticmethod
    def Create_room(**kwargs) -> Room:
        return Room.objects.create(
            **joinkwargs(
                {
                    "place": lambda: f"{random.choice(range(3 + 1))}{random.choice(list(range(99)))}",
                },
                kwargs
            )
        )
