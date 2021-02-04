import random

from django.test import TestCase

from apps.django.main.course.models import Subject
from apps.django.utils.tests_mixins import joinkwargs

SUBJECT_NAMES = [
    "Geschichte",
    "Deutsch",
    "Englisch",
    "Mathe",
    "Ethik",
    "Religion",
    "Sport",
    "Erdkunde",
    "Sozialkunde",
    "Informatik",
    "Französisch",
    "Italienisch",
    "Spanisch",
    "Griechisch",
]


class SubjectTestMixin(TestCase):
    @staticmethod
    def Create_subject(**kwargs) -> Subject:
        name = random.choice(SUBJECT_NAMES)
        
        return Subject.objects.create(
            **joinkwargs({
                "name": lambda: name,
                "short_name": lambda: name[:3]
            }, kwargs)
        )
