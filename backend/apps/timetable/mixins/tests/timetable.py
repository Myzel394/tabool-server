from abc import ABC
from datetime import date

from apps.lesson.mixins.tests import LessonTestMixin
from apps.utils.tests import joinkwargs, UserTestMixin
from ...models import Timetable

__all__ = [
    "TimetableTestMixin"
]


class TimetableTestMixin(
    LessonTestMixin,
    UserTestMixin,
    ABC
):
    @classmethod
    def Create_timetable(cls, **kwargs) -> Timetable:
        return Timetable.objects.create_with_lessons(
            **joinkwargs(
                {
                    "lessons_data": cls.Create_lessons_data,
                    "associated_user": cls.Create_user,
                    "school_year": lambda: date.today().year
                },
                kwargs
            )
        )
