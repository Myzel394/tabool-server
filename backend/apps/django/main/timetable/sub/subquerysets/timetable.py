from datetime import date
from typing import *

from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

from ...models.lesson import Lesson

if TYPE_CHECKING:
    from ...models import Timetable
    from apps.django.authentication.user.models import User

__all__ = [
    "TimetableQuerySet"
]


# noinspection PyTypeChecker
class TimetableQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: "User") -> "TimetableQuerySet":
        lessons = Lesson.objects.from_user(user)
        timetable_ids = lessons \
            .values_list("timetable", flat=True) \
            .distinct()
        timetables = self.only("id").filter(id__in=timetable_ids)
        
        return timetables
    
    def current(self, user: "User") -> "Timetable":
        today = date.today()
        timetables = self \
            .from_user(user) \
            .only("start_date", "end_date") \
            .filter(start_date__lte=today, end_date__gte=today)
        current_timetable = timetables.first()
        
        return current_timetable
