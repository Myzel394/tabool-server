import random
from datetime import datetime, timedelta

from apps.django.main.lesson.mixins.tests import *
from apps.django.main.lesson.models import *
from apps.django.utils.tests import *
from apps.utils.dates import find_next_date_by_weekday
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
