import random
from abc import ABC
from datetime import datetime, timedelta

from apps.lesson.mixins.tests import LessonTestMixin
from apps.lesson.models import LessonData
from apps.utils.date import find_next_date_by_weekday
from apps.utils.tests import joinkwargs
from ...models import Homework


class HomeworkTestMixin(LessonTestMixin, ABC):
    @staticmethod
    def get_random_due_date() -> datetime:
        return find_next_date_by_weekday(
            (datetime.now() + (
                # Days
                random.choice([
                    timedelta(days=x) for x in [0, 1, 2, 3, 4, 5, 10, 12, 14]
                ])
            )
             ).date(),
            random.choice(LessonData.objects.all().values_list("weekday", flat=True).distinct())
        )
    
    @classmethod
    def Create_homework(cls, **kwargs) -> Homework:
        return Homework.objects.create(
            **joinkwargs(
                {
                    "lesson": cls.Create_lesson,
                    "due_date": cls.get_random_due_date,
                },
                kwargs
            )
        )
