from django_common_utils.libraries.utils.text import create_short
from rest_framework import serializers

from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from apps.django.utils.serializers import (
    PreferredIdsMixin, RandomIDSerializerMixin, UserRelationField,
    WritableSerializerMethodField,
)
from .user_relations import UserHomeworkRelationSerializer
from ...models import Homework

__all__ = [
    "HomeworkListSerializer", "HomeworkDetailSerializer"
]


class HomeworkListSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "homework"
    
    class Meta:
        model = Homework
        fields = [
            "lesson", "due_date", "created_at", "id", "truncated_information"
        ]
    
    lesson = LessonField()
    
    truncated_information = serializers.SerializerMethodField()
    
    def get_truncated_information(self, instance: Homework) -> str:
        return create_short(instance.information) if instance.information else None


class HomeworkDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "homework"
    
    class Meta:
        model = Homework
        fields = [
            "lesson", "is_private", "due_date", "information", "type", "created_at", "id", "user_relation"
        ]
        read_only_fields = [
            "created_at", "id", "user_relation"
        ]
    
    is_private = WritableSerializerMethodField(
        deserializer_field=serializers.BooleanField()
    )
    
    lesson = LessonField(detail=True)
    
    user_relation = UserRelationField(UserHomeworkRelationSerializer)
    
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
