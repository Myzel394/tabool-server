from django.conf import settings
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

from ...models.lesson import Lesson

__all__ = [
    "TimetableQuerySet"
]


# noinspection PyTypeChecker
class TimetableQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "TimetableQuerySet":
        lessons = Lesson.objects.from_user(user)
        timetable_ids = lessons \
            .values_list("timetable", flat=True) \
            .distinct()
        timetables = self.only("id").filter(id__in=timetable_ids)
        
        return timetables
