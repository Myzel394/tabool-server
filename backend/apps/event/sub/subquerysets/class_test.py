from django.conf import settings
from django_common_utils.libraries.models import CustomQuerySetMixin

__all__ = [
    "ClassTestQuerySet"
]


class ClassTestQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "ClassTestQuerySet":
        return self.filter(course__associated_user=user)
