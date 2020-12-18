from typing import *

from django_common_utils.libraries.utils.text import create_short
from rest_framework import serializers

from apps.django.main.lesson.public.serializer_fields.course import CourseField
from apps.django.main.school_data.public.serializer_fields.room import RoomField
from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin
from ...models import Exam

__all__ = [
    "ExamListSerializer", "ExamDetailSerializer"
]


class ExamListSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "exam"
    
    class Meta:
        model = Exam
        fields = [
            "course", "targeted_date", "truncated_information", "id"
        ]
    
    course = CourseField()
    
    truncated_information = serializers.SerializerMethodField()
    
    def get_truncated_information(self, instance: Exam) -> Optional[str]:
        return create_short(instance.information) if instance.information else None


class ExamDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "exam"
    
    class Meta:
        model = Exam
        fields = [
            "course", "room", "targeted_date", "information", "created_at", "id"
        ]
        read_only_fields = [
            "created_at"
        ]
    
    course = CourseField(detail=True)
    room = RoomField(required=False, detail=True)
