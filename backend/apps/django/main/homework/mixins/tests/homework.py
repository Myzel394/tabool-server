import random
from datetime import date, datetime, timedelta

import lorem

from apps.django.main.homework.models import Homework
from apps.django.main.timetable.mixins import joinkwargs, Lesson, LessonTestMixin
from apps.utils import find_next_date_by_weekday

__all__ = [
    "HomeworkTestMixin"
]


class HomeworkTestMixin(LessonTestMixin):
    @classmethod
    def get_random_due_date(cls) -> datetime:
        weekdays = Lesson.objects.all().values_list("weekday", flat=True).distinct()
        
        if len(weekdays) == 0:
            weekdays = [cls.Create_lesson().weekday]
        
        return find_next_date_by_weekday(
            (datetime.now() + (
                # Days
                random.choice([
                    timedelta(days=x) for x in [0, 1, 2, 3, 4, 5, 10, 12, 14]
                ])
            )
             ).date(),
            random.choice(weekdays)
        )
    
    @classmethod
    def Create_homework(cls, **kwargs) -> Homework:
        """

        :rtype: object
        """
        lesson = kwargs.pop("lesson", None) or cls.Create_lesson()
        
        return Homework.objects.create(
            **joinkwargs({
                "due_date": lambda: find_next_date_by_weekday(date.today(), lesson.weekday),
                "information": lorem.text,
                **cls.Create_lesson_argument(lesson, kwargs.pop("lesson_date", None))
            }, kwargs)
        )
