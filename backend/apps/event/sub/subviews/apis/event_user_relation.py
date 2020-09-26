from apps.utils.viewsets import UserRelationViewSetMixin
from ....models import Event
from ....serializers import UserEventRelationSerializer


class UserEventRelationViewSet(UserRelationViewSetMixin):
    serializer_class = UserEventRelationSerializer
    model = Event
