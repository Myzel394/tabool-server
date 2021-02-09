from typing import *

from rest_framework import serializers

from .base import BaseTimetableSerializer
from ..lesson import StudentDetailLessonSerializer, TeacherDetailLessonSerializer

if TYPE_CHECKING:
    from ....models import Timetable

__all__ = [
    "DetailTimetableSerializer"
]


class DetailTimetableSerializer(BaseTimetableSerializer):
    class Meta(BaseTimetableSerializer.Meta):
        fields = [
            "lessons",
        ]
    
    lessons = serializers.SerializerMethodField()
    
    def get_lessons(self, instance: "Timetable") -> list:
        if self.context["request"].user.is_student:
            return StudentDetailLessonSerializer(instance=instance.lessons, many=True, context=self.context).data
        return TeacherDetailLessonSerializer(instance=instance.lessons, many=True, context=self.context).data
