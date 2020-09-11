import random
import names

from django.test import TestCase
from abc import ABC

from ..models import Teacher


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
    