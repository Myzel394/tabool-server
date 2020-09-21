from abc import ABC

from apps.subject.mixins.tests import LessonTestMixin
from apps.utils.tests import UserCreationTestMixin
from ...models import TimeTable

__all__ = [
    "TimeTableTestMixin"
]


class TimeTableTestMixin(
    LessonTestMixin,
    UserCreationTestMixin,
    ABC
):
    @classmethod
    def Create_timetable(cls, **kwargs) -> TimeTable:
        return TimeTable.objects.create_with_lessons(
            **{
                "lessons": cls.Create_lessons(),
                **kwargs
            }
        )
