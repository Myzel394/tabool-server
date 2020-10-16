from apps.django.utils.serializers import RandomIDSerializerMixin, UserRelationField
from .user_relations import UserLessonRelationSerializer
from ...models import Lesson
from ...public.serializer_fields import LessonDataField

__all__ = [
    "LessonListSerializer", "LessonDetailSerializer", "LessonDetailSerializer"
]


class LessonListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Lesson
        fields = [
            "lesson_data", "date", "id"
        ]
    
    lesson_data = LessonDataField()


class LessonDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Lesson
        fields = [
            "lesson_data", "date", "id", "user_relation"
        ]
    
    user_relation = UserRelationField(UserLessonRelationSerializer)
    
    lesson_data = LessonDataField()
