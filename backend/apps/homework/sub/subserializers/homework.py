from rest_framework import serializers

from apps.lesson.public.serializer_fields import LessonField
from apps.utils.serializers import RandomIDSerializerMixin, WritableSerializerMethodField
from .user_relations import UserHomeworkRelationSerializer
from ...models import Homework

__all__ = [
    "HomeworkListSerializer", "HomeworkDetailSerializer"
]


class HomeworkListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Homework
        fields = [
            "lesson", "due_date", "id"
        ]
    
    lesson = LessonField()


class HomeworkDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Homework
        fields = [
            "lesson", "is_private", "due_date", "information", "type", "created_at", "edited_at", "id", "user_relation"
        ]
        read_only_fields = [
            "created_at", "edited_at", "id", "user_relation"
        ]
    
    is_private = WritableSerializerMethodField(
        deserializer_field=serializers.BooleanField()
    )
    
    lesson = LessonField()
    
    user_relation = UserHomeworkRelationSerializer(read_only=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_private = False
    
    def create(self, validated_data):
        validated_data["private_to_user"] = self.context["request"].user if self._is_private else None
        
        return super().create(validated_data)
    
    @staticmethod
    def get_is_private(obj: Homework):
        return obj.is_private
    
    def set_is_private(self, value: bool):
        self._is_private = value
