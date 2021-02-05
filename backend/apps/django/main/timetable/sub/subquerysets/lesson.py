from django.conf import settings
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

from apps.django.main.course.models import Course

__all__ = [
    "LessonQuerySet"
]


# noinspection PyTypeChecker
class LessonQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "LessonQuerySet":
        course_ids = Course.objects \
            .from_user(user) \
            .values_list("id", flat=True) \
            .distinct()
        lessons = self \
            .only("course") \
            .filter(course__id__in=course_ids)
        
        return lessons
