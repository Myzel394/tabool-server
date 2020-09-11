from typing import *

from django_common_utils.libraries.models import CustomQuerySetMixin

if TYPE_CHECKING:
    from .. import TimeTable


class TimeTableQuerySet(CustomQuerySetMixin.QuerySet):
    def create_with_lessons(self, **kwargs) -> "TimeTable":
        lessons = kwargs.pop("lessons")
        
        timetable = self.create(
            **kwargs
        )
        timetable.lessons.add(lessons)
        
        return timetable
