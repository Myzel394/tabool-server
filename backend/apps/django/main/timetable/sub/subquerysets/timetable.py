from django.conf import settings
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

from apps.django.main.course.models import Course
from ...models import Lesson

__all__ = [
    "TimetableQuerySet"
]


# noinspection PyTypeChecker
class TimetableQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "TimetableQuerySet":
        course_ids = Course.objects \
            .from_user(user) \
            .values_list("id", flat=True) \
            .distinct()
        lessons = Lesson.objects \
            .only("lesson") \
            .filter(lesson__course__id__in=course_ids)
        timetable_ids = lessons \
            .values_list("id", flat=True) \
            .distinct()
        timetables = self.only("id").filter(id__in=timetable_ids)
        
        return timetables
