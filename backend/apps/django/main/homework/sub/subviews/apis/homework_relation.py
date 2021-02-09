from apps.django.utils.permissions import AuthenticationAndActivePermission, IsStudent
from apps.django.utils.viewsets import UserRelationViewSetMixin
from ....models import Homework, UserHomeworkRelation
from ....serializers import UserHomeworkRelationSerializer

__all__ = [
    "UserHomeworkRelationViewSet"
]


class UserHomeworkRelationViewSet(UserRelationViewSetMixin):
    permission_classes = [AuthenticationAndActivePermission & IsStudent]
    serializer_class = UserHomeworkRelationSerializer
    model = Homework
    relation_model = UserHomeworkRelation
