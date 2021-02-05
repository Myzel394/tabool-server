from django.conf import settings
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

from apps.django.main.timetable.models import Lesson

__all__ = [
    "ClassbookQuerySet"
]


# noinspection PyTypeChecker
class ClassbookQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "ClassbookQuerySet":
        lessons = Lesson.objects.from_user(user)
        return self \
            .only("lesson") \
            .filter(lesson__in=lessons)
