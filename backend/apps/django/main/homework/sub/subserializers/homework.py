from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.utils.text import create_short
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from apps.django.main.school_data.sub.subserializers.subject import SubjectDetailSerializer
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
            "lesson", "due_date", "created_at", "id", "truncated_information", "subject"
        ]
    
    lesson = LessonField()
    subject = serializers.SerializerMethodField()
    
    truncated_information = serializers.SerializerMethodField()
    
    def get_truncated_information(self, instance: Homework) -> str:
        return create_short(instance.information) if instance.information else None
    
    def get_subject(self, instance: Homework):
        return SubjectDetailSerializer(instance=instance.lesson.lesson_data.course.subject, context=self.context).data


class HomeworkDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "homework"
    instance: Homework
    
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
    
    @staticmethod
    def get_is_private(obj: Homework):
        return obj.is_private
    
    def set_is_private(self, value: bool):
        self._is_private = value
    
    def create(self, validated_data):
        validated_data["private_to_user"] = self.context["request"].user if self._is_private else None
        
        return super().create(validated_data)
    
    def validate(self, attrs):
        if self.instance and not self.instance.is_private and self._is_private:
            raise ValidationError({
                "is_private": _("Öffentliche Hausaufgaben können nicht privat gestellt werden.")
            })
        
        return super().validate(attrs)
