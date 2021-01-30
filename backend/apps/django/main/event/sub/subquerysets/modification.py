from django.conf import settings
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

__all__ = [
    "ModificationQuerySet"
]


# noinspection PyTypeChecker
class ModificationQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "ModificationQuerySet":
        return self.filter(lesson__course__participants__in=[user])
