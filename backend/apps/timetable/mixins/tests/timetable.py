from abc import ABC

from apps.subject.mixins.tests import LessonTestMixin
from apps.utils.tests import joinkwargs, UserCreationTestMixin
from ...models import Timetable

__all__ = [
    "TimetableTestMixin"
]


class TimetableTestMixin(
    LessonTestMixin,
    UserCreationTestMixin,
    ABC
):
    @classmethod
    def Create_timetable(cls, **kwargs) -> Timetable:
        return Timetable.objects.create_with_lessons(
            **joinkwargs(
                {
                    "lessons_data": cls.Create_lessons_data,
                },
                kwargs
            )
        )
