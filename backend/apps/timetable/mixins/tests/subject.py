import random
from abc import ABC

from django.test import TestCase

from ...models import Subject

__all__ = [
    "SubjectTestMixin"
]


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
