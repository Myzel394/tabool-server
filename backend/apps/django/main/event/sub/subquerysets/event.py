from typing import *

from django_common_utils.libraries.models.mixins import CustomQuerySetMixin

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User

__all__ = [
    "EventQuerySet"
]


# noinspection PyTypeChecker
class EventQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: "User") -> "EventQuerySet":
        return self
