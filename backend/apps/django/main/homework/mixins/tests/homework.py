import random
from datetime import datetime, timedelta

from apps.django.main.lesson.mixins.tests import *
from apps.django.main.lesson.models import Lesson
from apps.django.utils.tests_mixins import *
from apps.utils.dates import find_next_date_by_weekday
from ...models import Homework


class HomeworkTestMixin(LessonTestMixin, ABC):
    @classmethod
    def get_random_due_date(cls, lesson: Lesson) -> datetime:
        return find_next_date_by_weekday(
            (datetime.now() + (
                # Days
                random.choice([
                    timedelta(days=x) for x in [0, 1, 2, 3, 4, 5, 10, 12, 14]
                ])
            )
             ).date(),
            lesson.weekday
        )
    
    @classmethod
    def Create_homework(cls, **kwargs) -> Homework:
        lesson = kwargs.pop("lesson", cls.Create_lesson())
        
        return Homework.objects.create(
            **joinkwargs(
                {
                    "lesson": lambda: lesson,
                    "due_date": lambda: cls.get_random_due_date(lesson),
                },
                kwargs
            )
        )
