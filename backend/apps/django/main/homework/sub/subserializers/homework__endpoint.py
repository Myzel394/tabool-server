from django_common_utils.libraries.utils.text import create_short
from rest_framework import serializers

from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from apps.django.main.school_data.sub.subserializers.subject import SubjectDetailSerializer
from apps.django.utils.serializers import (
    PreferredIdsMixin, RandomIDSerializerMixin,
)
from .homework import HomeworkDetailSerializer as BaseHomeworkDetailSerializer
from ...models import Homework

__all__ = [
    "HomeworkListSerializer", "HomeworkDetailEndpointSerializer"
]


class HomeworkListSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "homework"
    
    class Meta:
        model = Homework
        fields = [
            "lesson", "due_date", "created_at", "id", "truncated_information", "subject"
        ]
    
    lesson = LessonField()
    subject = serializers.SerializerMethodField()
    
    truncated_information = serializers.SerializerMethodField()
    
    def get_truncated_information(self, instance: Homework) -> str:
        return create_short(instance.information) if instance.information else None
    
    def get_subject(self, instance: Homework):
        return SubjectDetailSerializer(instance=instance.lesson.lesson_data.course.subject, context=self.context).data


class HomeworkDetailEndpointSerializer(BaseHomeworkDetailSerializer):
    class Meta:
        model = Homework
        fields = [
            "lesson", "is_private", "due_date", "information", "type", "created_at", "id", "user_relation",
            "truncated_information"
        ]
        read_only_fields = [
            "created_at", "id", "user_relation"
        ]
    
    truncated_information = serializers.SerializerMethodField()
    
    lesson = LessonField(detail=True)
    
    def get_truncated_information(self, instance: Homework) -> str:
        return create_short(instance.information) if instance.information else None
