from django.conf import settings
from django_common_utils.libraries.models import CustomQuerySetMixin

__all__ = [
    "SubjectQuerySet"
]


# noinspection PyTypeChecker
class SubjectQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "SubjectQuerySet":
        return self.only("associated_user").filter(associated_user=user)
