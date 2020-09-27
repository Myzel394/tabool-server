from apps.utils.viewsets import UserRelationViewSetMixin

from ....models import Event
from ....serializers import UserEventRelationSerializer

__all__ = [
    "EventUserRelationViewSet"
]


class EventUserRelationViewSet(UserRelationViewSetMixin):
    serializer_class = UserEventRelationSerializer
    model = Event
