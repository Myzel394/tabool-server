from apps.relation_managers.serializers import UserRelationSerializerField
from apps.utils.serializers import RandomIDSerializerMixin
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
        read_only = [
            "lesson_data", "date", "id", "user_relation"
        ]
    
    user_relation = UserRelationSerializerField(serializer_class=UserLessonRelationSerializer)
    
    lesson_data = LessonDataField()
