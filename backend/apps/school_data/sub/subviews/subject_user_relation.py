from apps.utils.viewsets import UserRelationViewSetMixin
from ...models import Subject
from ...serializers import UserSubjectRelationSerializer

__all__ = [
    "UserSubjectRelationViewSet"
]


class UserSubjectRelationViewSet(UserRelationViewSetMixin):
    serializer_class = UserSubjectRelationSerializer
    model = Subject
