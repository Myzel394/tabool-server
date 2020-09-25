from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from apps.authentication.sub.subserializers import UserDetailSerializer
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
            "lesson", "due_date", "completed", "id"
        ]
    
    lesson = LessonDetailSerializer()


class HomeworkDetailSerializer(RandomIDSerializerMixin, WritableNestedModelSerializer):
    class Meta:
        model = Homework
        fields = [
            "lesson", "is_private", "due_date", "information", "completed",
            "type", "id", "created_at", "edited_at",
        ]
    
    lesson = LessonDetailSerializer()
    is_private = WritableSerializerMethodField(
        deserializer_field=serializers.BooleanField()
    )
    
    def get_is_private(self, obj: Homework):
        return obj.is_private
    
    def set_is_private(self, value: bool):
        self.instance.private_for_user = CurrentUserDefault() if value else None

