from django.conf import settings
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

__all__ = [
    "LessonQuerySet"
]


class LessonQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "LessonQuerySet":
        return self.filter(lesson_data__course__participants__in=[user])
