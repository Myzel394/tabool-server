from typing import *

from django_common_utils.libraries.utils import create_short
from rest_framework import serializers

from apps.django.main.timetable.sub.subserializers.lesson import DetailLessonSerializer
from .base import BaseHomeworkSerializer
from ....models import Homework

__all__ = [
    "ListHomeworkSerializer"
]


class ListHomeworkSerializer(BaseHomeworkSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "due_date", "id", "truncated_information",
        ]
    
    lesson = DetailLessonSerializer()
    
    truncated_information = serializers.SerializerMethodField()
    
    @staticmethod
    def get_truncated_information(instance: Homework) -> Optional[str]:
        if instance.information:
            return create_short(instance.information)
        return
