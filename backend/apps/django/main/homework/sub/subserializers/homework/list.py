from typing import *

from django_common_utils.libraries.utils import create_short
from rest_framework import serializers

from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from apps.django.main.school_data.sub.subserializers.subject import SubjectSerializer
from .base import BaseHomeworkSerializer
from ....models import Homework

__all__ = [
    "ListHomeworkSerializer"
]


class ListHomeworkSerializer(BaseHomeworkSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "lesson", "due_date", "created_at", "id", "truncated_information", "subject"
        ]
    
    lesson = LessonField()
    
    truncated_information = serializers.SerializerMethodField()
    
    @staticmethod
    def get_truncated_information(instance: Homework) -> Optional[str]:
        if instance.information:
            return create_short(instance.information)
        return
    
    @staticmethod
    def get_subject(instance: Homework):
        return SubjectSerializer(instance=instance.lesson.lesson_data.course.subject, context=self.context).data
