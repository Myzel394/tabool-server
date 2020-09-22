from django.conf import settings
from django_common_utils.libraries.models import CustomQuerySetMixin


__all__ = [
    "LessonQuerySet"
]


# noinspection PyTypeChecker
class LessonQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "LessonQuerySet":
        return self.filter(lesson_data__associated_user=user)
