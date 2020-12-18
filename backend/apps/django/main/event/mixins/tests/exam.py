import random
from datetime import date

import lorem

from apps.django.main.lesson.mixins.tests import *
from apps.django.main.school_data.mixins.tests import *
from apps.django.utils.tests import *
from apps.utils.dates import find_next_date_by_weekday
from ...models import Exam


class ExamTestMixin(RoomTestMixin, CourseTestMixin, SubjectTestMixin, ABC):
    @classmethod
    def create_exam(cls, **kwargs) -> Exam:
        return Exam.objects.create(
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
                kwargs
            )
        )
