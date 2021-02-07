from apps.django.utils.viewsets import UserRelationViewSetMixin
from ....models import Homework, UserHomeworkRelation
from ....serializers import UserHomeworkRelationSerializer

__all__ = [
    "UserHomeworkRelationViewSet"
]


class UserHomeworkRelationViewSet(UserRelationViewSetMixin):
    serializer_class = UserHomeworkRelationSerializer
    model = Homework
    relation_model = UserHomeworkRelation
