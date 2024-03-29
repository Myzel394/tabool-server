from apps.django.utils.viewsets import UserRelationViewSetMixin
from ....models import Subject, UserSubjectRelation
from ....serializers import UserSubjectRelationSerializer

__all__ = [
    "UserSubjectRelationViewSet"
]


class UserSubjectRelationViewSet(UserRelationViewSetMixin):
    serializer_class = UserSubjectRelationSerializer
    model = Subject
    relation_model = UserSubjectRelation
