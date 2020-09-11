import random

from django.test import TestCase
from abc import ABC

from ..models import Subject


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
