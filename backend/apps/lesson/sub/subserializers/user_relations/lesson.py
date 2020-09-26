from apps.utils.serializers import RandomIDSerializerMixin
from ....models import UserLessonRelation

__all__ = [
    "UserLessonRelationSerializer"
]


class UserLessonRelationSerializer(RandomIDSerializerMixin):
    class Meta:
        model = UserLessonRelation
        fields = [
            "attendance"
        ]
