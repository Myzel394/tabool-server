import random
from abc import ABC

import names
from django.test import TestCase

from apps.utils.tests import joinkwargs
from ...models import Teacher

__all__ = [
    "TeacherTestMixin"
]


class TeacherTestMixin(TestCase, ABC):
    @staticmethod
    def Create_teacher(**kwargs) -> Teacher:
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        return Teacher.objects.create(
            **joinkwargs(
                {
                    "first_name": lambda: first_name,
                    "last_name": lambda: last_name,
                    "email": lambda: (
                        f"{first_name}.{last_name}@gmail.com"
                        if random.choice([True, False]) else
                        None
                    ),
                },
                kwargs
            )
        )
