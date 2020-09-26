from apps.utils.viewsets import UserRelationViewSetMixin
from ....models import Lesson
from ....serializers import UserLessonRelationSerializer

__all__ = [
    "UserLessonRelationViewSet"
]


class UserLessonRelationViewSet(UserRelationViewSetMixin):
    serializer_class = UserLessonRelationSerializer
    model = Lesson
