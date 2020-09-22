from django.conf import settings
from django_common_utils.libraries.models import CustomQuerySetMixin

__all__ = [
    "LessonDataQuerySet"
]


# noinspection PyTypeChecker
class LessonDataQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "LessonDataQuerySet":
        return self.only("associated_user").filter(associated_user=user)
