import random
from abc import ABC
from datetime import datetime, timedelta

from apps.subject.mixins.tests import LessonTestMixin
from apps.subject.models import LessonData
from apps.utils.date import find_next_date_by_weekday
from ...models import TeacherHomework, UserHomework


class HomeworkTestMixin(LessonTestMixin, ABC):
    @staticmethod
    def get_random_due_date() -> datetime:
        return find_next_date_by_weekday(
            datetime.now() + (
                # Minutes
                random.choice([
                    timedelta(hours=2), timedelta(hours=12), timedelta(hours=16)
                ])
            ) + (
                # Days
                random.choice([
                    timedelta(days=x) for x in [0, 1, 2, 3, 4, 5, 10, 12, 14]
                ])
            ),
            random.choice(LessonData.objects.all().values_list("weekday", flat=True).distinct())
        )
    
    # TODO: Test für Allowed weekdays machen, Test für zufällige Daten machen.
    
    @classmethod
    def Create_teacher_homework(cls, **kwargs) -> TeacherHomework:
        return TeacherHomework.objects.create(
            **{
                "lesson": cls.Create_lesson(),
                "due_date": cls.get_random_due_date(),
                **kwargs
            }
        )
    
    @classmethod
    def Create_user_homework(cls, **kwargs) -> UserHomework:
        return UserHomework.objects.create(
            **{
                "lesson": cls.Create_lesson(),
                "due_date": cls.get_random_due_date(),
                **kwargs
            }
        )
