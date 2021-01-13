from apps.django.utils.viewsets import UserRelationViewSetMixin
from ....models import Event, UserEventRelation
from ....serializers import UserEventRelationSerializer

__all__ = [
    "EventUserRelationViewSet"
]


class EventUserRelationViewSet(UserRelationViewSetMixin):
    serializer_class = UserEventRelationSerializer
    model = Event
    relation_model = UserEventRelation
