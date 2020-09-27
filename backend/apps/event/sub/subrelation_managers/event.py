from typing import *

from django.contrib.auth import get_user_model

from apps.authentication.public import *
from apps.relation_managers.managers import RelationManagerMixin
from ...models import Event

__all__ = [
    "EventRelationManager"
]


class EventRelationManager(RelationManagerMixin):
    class Meta:
        model = Event
    
    def get_users(self) -> List[USER]:
        model = get_user_model()
        return model.objects.all().only("is_active").filter(is_active=True)
    
    def create_relations(self) -> None:
        users = self.get_users()
        
        Event.objects.manage_relations(users, self.instance)
