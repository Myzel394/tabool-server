from django.conf import settings
from django_common_utils.libraries.models import CustomQuerySetMixin

__all__ = [
    "EventUserOptionQuerySet"
]


class EventUserOptionQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "EventUserOptionQuerySet":
        return self.only("associated_user").filter(associated_user=user)
