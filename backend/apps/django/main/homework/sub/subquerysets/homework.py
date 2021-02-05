from django.conf import settings
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

from apps.django.main.timetable.models import Lesson

__all__ = [
    "HomeworkQuerySet"
]


# noinspection PyTypeChecker
class HomeworkQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "HomeworkQuerySet":
        lessons = Lesson.objects.from_user(user)
        return self \
            .only("lesson") \
            .filter(lesson__in=lessons)
