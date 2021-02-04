from typing import *

from rest_framework import serializers

from .base import BaseTimetableSerializer
from ..lesson import DetailLessonSerializer

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
    
    @staticmethod
    def get_lessons(instance: "Timetable") -> list:
        return DetailLessonSerializer(instance=instance.lessons, many=True).data
