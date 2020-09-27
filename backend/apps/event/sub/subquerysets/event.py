from typing import *

from django.conf import settings
from django_common_utils.libraries.models import CustomQuerySetMixin

from ...models.user_relations.event import UserEventRelation

if TYPE_CHECKING:
    from ...models import Event

__all__ = [
    "EventQuerySet"
]


class EventQuerySet(CustomQuerySetMixin.QuerySet):
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "EventQuerySet":
        return self.filter(usereventrelation__user=user)
    
    def manage_relations(self, users: list, instance: "Event") -> None:
        for user in users:
            UserEventRelation.objects.get_or_create(
                user=user,
                event=instance
            )
