from apps.django.utils.relation_managers.managers import SimpleAllUserRelationManagerMixin
from ...models import Event

__all__ = [
    "EventRelationManager"
]


class EventRelationManager(SimpleAllUserRelationManagerMixin):
    class Meta:
        model = Event
