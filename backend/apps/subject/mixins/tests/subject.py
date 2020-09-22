import random
from abc import ABC

from apps.utils.tests import UserCreationTestMixin
from ...models import Subject

__all__ = [
    "SubjectTestMixin"
]


class SubjectTestMixin(UserCreationTestMixin, ABC):
    @classmethod
    def Create_subject(cls, **kwargs) -> Subject:
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
                "associated_user": getattr(cls, "associated_user", None) or cls.Create_user(),
                **kwargs
            }
        )
