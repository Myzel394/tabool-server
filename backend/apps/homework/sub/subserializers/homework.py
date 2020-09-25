from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from apps.lesson.sub.subserializers.lesson import LessonDetailSerializer
from apps.utils.serializers import RandomIDSerializerMixin, WritableSerializerMethodField
from ...models import Homework

__all__ = [
    "HomeworkListSerializer", "HomeworkDetailSerializer"
]


class HomeworkListSerializer(RandomIDSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = [
            "lesson", "due_date", "id"
        ]
    
    lesson = LessonDetailSerializer()


class HomeworkDetailSerializer(RandomIDSerializerMixin, WritableNestedModelSerializer):
    class Meta:
        model = Homework
        fields = [
            "lesson", "is_private", "due_date", "information", "type", "id", "created_at", "edited_at",
        ]
        read_only_fields = [
            "created_at", "edited_at",
        ]
    
    lesson = LessonDetailSerializer()
    is_private = WritableSerializerMethodField(
        deserializer_field=serializers.BooleanField()
    )
    
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
