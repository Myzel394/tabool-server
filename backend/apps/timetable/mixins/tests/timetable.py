from abc import ABC

from apps.utils.tests import UserCreationTestMixin
from . import RandomLessonTextMixin
from ...models import TimeTable

__all__ = [
    "TimeTableTestMixin"
]


class TimeTableTestMixin(
    RandomLessonTextMixin,
    UserCreationTestMixin,
    ABC
):
    @classmethod
    def Create_timetable(cls, **kwargs) -> TimeTable:
        return TimeTable.objects.create_with_lessons(
            **{
                "lessons": cls.Create_lessons(),
                "associated_user": cls.Create_user(),
                **kwargs
            }
        )
