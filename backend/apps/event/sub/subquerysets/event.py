from django.conf import settings
from django_common_utils.libraries.models import CustomQuerySetMixin

from apps.utils.querysets import RelationAllUserQuerySetMixin
from ...models.user_relations.event import UserEventRelation

__all__ = [
    "EventQuerySet"
]


class EventQuerySet(CustomQuerySetMixin.QuerySet, RelationAllUserQuerySetMixin):
    related_model = UserEventRelation
    
    def from_user(self, user: settings.AUTH_USER_MODEL) -> "EventQuerySet":
        return self.filter(usereventrelation__user=user)
