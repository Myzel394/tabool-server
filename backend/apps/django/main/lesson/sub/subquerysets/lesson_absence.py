from django.conf import settings
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

__all__ = [
    "LessonAbsenceQuerySet"
]


class LessonAbsenceQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "LessonAbsenceQuerySet":
        return self.filter(associated_user=user)
