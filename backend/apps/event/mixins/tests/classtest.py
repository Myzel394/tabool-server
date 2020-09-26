import random
from abc import ABC
from datetime import date

import lorem

from apps.lesson.mixins.tests import RoomTestMixin, SubjectTestMixin
from apps.lesson.mixins.tests.course import CourseTestMixin
from apps.utils import joinkwargs
from apps.utils.date import find_next_date_by_weekday
from ...models import Classtest


class ClasstestTestMixin(RoomTestMixin, CourseTestMixin, SubjectTestMixin, ABC):
    @classmethod
    def Create_classtest(cls, **kwargs) -> Classtest:
        return Classtest.objects.create(
            **joinkwargs(
                {
                    "course": cls.Create_course,
                    "room": cls.Create_room,
                    "targeted_date": lambda: find_next_date_by_weekday(
                        date.today(),
                        random.choice([0, 1, 2, 3, 4])
                    ),
                    "information": lambda: random.choice([None, lorem.sentence()]),
                },
                kwargs  # TODO: Add joinkwargs everywhere!
            )
        )
