from typing import *

from django.conf import settings
from django_common_utils.libraries.models import CustomQuerySetMixin

from apps.subject.models import LessonData

if TYPE_CHECKING:
    from apps.timetable import TimeTable

__all__ = [
    "TimeTableQuerySet"
]


class TimeTableQuerySet(CustomQuerySetMixin.QuerySet):
    def create_with_lessons(self, **kwargs) -> "TimeTable":
        lessons = kwargs.pop("lessons_data")
        
        timetable = self.create(
            **kwargs
        )
        timetable.lessons_data.add(*lessons)
        
        return timetable
    
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "TimeTableQuerySet":
        return self.only("lessons_data").filter(
            lessons_data__in=LessonData.objects.from_user(user)
        ).distinct()
