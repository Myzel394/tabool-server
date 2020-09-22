import random
from abc import ABC
from datetime import date

import lorem

from apps.subject.mixins.tests import RoomTestMixin, SubjectTestMixin
from apps.utils.date import find_next_date_by_weekday
from ...models import ClassTest


class ClassTestTestMixin(RoomTestMixin, SubjectTestMixin, ABC):
    @classmethod
    def Create_class_test(cls, **kwargs) -> ClassTest:
        return ClassTest.objects.create(
            **{
                "subject": cls.Create_subject(),
                "room": cls.Create_room(),
                "targeted_date": find_next_date_by_weekday(
                    date.today(),
                    random.choice([0, 1, 2, 3, 4])
                ),
                "information": random.choice([None, lorem.sentence()]),
                **kwargs
            }
        )
