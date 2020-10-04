import random
from abc import ABC

from apps.utils.tests import joinkwargs, UserCreationTestMixin
from ...models import Subject

__all__ = [
    "SubjectTestMixin"
]


class SubjectTestMixin(UserCreationTestMixin, ABC):
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
