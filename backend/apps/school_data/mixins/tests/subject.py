import random
from abc import ABC

from apps.school_data.models import Subject
from apps.utils.tests import joinkwargs, UserTestMixin

__all__ = [
    "SubjectTestMixin"
]


class SubjectTestMixin(UserTestMixin, ABC):
    @classmethod
    def Create_subject(cls, **kwargs) -> Subject:
        choice = random.choice([
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
        ])
        
        return Subject.objects.create(
            **joinkwargs(
                {
                    "name": lambda: choice,
                    "short_name": lambda: choice[:2]
                },
                kwargs
            )
        )
