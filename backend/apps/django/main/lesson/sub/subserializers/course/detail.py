from typing import *

from rest_framework import serializers

from apps.django.main.school_data.public.serializer_fields.subject import SubjectField
from apps.django.main.school_data.public.serializer_fields.teacher import TeacherField
from .base import BaseCourseSerializer
from ....models import LessonData

if TYPE_CHECKING:
    from ....models import Course

__all__ = [
    "DetailCourseSerializer"
]


class DetailCourseSerializer(BaseCourseSerializer):
    class Meta(BaseCourseSerializer.Meta):
        fields = [
            "course_number", "participants_count", "weekdays", "subject", "teacher", "id"
        ]
    
    subject = SubjectField(detail=True)
    teacher = TeacherField(detail=True)
    
    participants_count = serializers.SerializerMethodField()
    weekdays = serializers.SerializerMethodField()
    
    @staticmethod
    def get_participants_count(obj: "Course"):
        return obj.participants.all().count()
    
    @staticmethod
    def get_weekdays(instance: "Course"):
        return list(set(
            LessonData.objects
                .only("course")
                .filter(course=instance)
                .values_list("weekday", flat=True)
        ))
