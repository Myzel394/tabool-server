from rest_framework import serializers

from apps.django.utils.serializers import ScoosoScraperSerializerMixin
from ....models import Lesson, LessonScoosoData

__all__ = [
    "LessonScoosoScraperSerializer"
]


class LessonScoosoScraperSerializer(ScoosoScraperSerializerMixin):
    class Meta:
        model = Lesson
        scooso_model = LessonScoosoData
        fields = [
            "time_id", "date", "video_conference_link"
        ]
    
    scooso_id = None
    time_id = serializers.IntegerField(min_value=0)
    
    date = serializers.DateField()
    
    def get_unique_data(self, validated_data: dict) -> dict:
        return {
            "lesson_data": validated_data["lesson_data"],
            "date": validated_data["date"]
        }
    
    def pop_scooso_data(self, validated_data: dict) -> dict:
        return {
            "time_id": validated_data.pop("time_id")
        }
