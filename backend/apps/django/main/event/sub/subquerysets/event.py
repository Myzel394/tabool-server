from django.conf import settings
from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

__all__ = [
    "EventQuerySet"
]


class EventQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "EventQuerySet":
        return self.filter(usereventrelation__user=user)
