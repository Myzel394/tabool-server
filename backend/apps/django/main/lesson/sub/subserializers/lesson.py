from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin, UserRelationField
from .classbook import ClassbookDetailSerializer
from .lesson_data import LessonDataDetailSerializer, LessonDataListSerializer
from .user_relations import UserLessonRelationSerializer
from ...models import Lesson

__all__ = [
    "LessonListSerializer", "LessonDetailSerializer", "LessonDetailSerializer", "LessonTimetableSerializer"
]


class LessonListSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "lesson"
    
    class Meta:
        model = Lesson
        fields = [
            "lesson_data", "date", "id"
        ]
    
    lesson_data = LessonDataListSerializer()


class LessonDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "lesson"
    
    class Meta:
        model = Lesson
        fields = [
            "lesson_data", "date", "id", "user_relation", "classbook"
        ]
    
    user_relation = UserRelationField(UserLessonRelationSerializer)
    
    lesson_data = LessonDataDetailSerializer()
    classbook = ClassbookDetailSerializer()


class LessonTimetableSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "lesson"
    
    class Meta:
        model = Lesson
        fields = [
            "lesson_data", "date", "id"
        ]
    
    lesson_data = LessonDataDetailSerializer()
