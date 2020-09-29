from django.conf import settings
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

__all__ = [
    "CourseQuerySet"
]


# noinspection PyTypeChecker
class CourseQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "CourseQuerySet":
        return self.only("participants").filter(participants__in=[user])
