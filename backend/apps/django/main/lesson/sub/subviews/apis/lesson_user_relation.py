from apps.django.utils.viewsets import UserRelationViewSetMixin
from ....models import Lesson, UserLessonRelation
from ....serializers import UserLessonRelationSerializer

__all__ = [
    "UserLessonRelationViewSet"
]


class UserLessonRelationViewSet(UserRelationViewSetMixin):
    serializer_class = UserLessonRelationSerializer
    model = Lesson
    relation_model = UserLessonRelation
