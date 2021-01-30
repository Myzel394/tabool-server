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
    lesson_type = serializers.UUIDField()
    
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    date = serializers.DateField()
    
    def get_unique_data(self, validated_data: dict) -> dict:
        return {
            "date": validated_data["date"],
            "start_time": validated_data["start_time"],
            "end_time": validated_data["end_time"],
            "weekday": validated_data["date"].weekday(),
            
            "course": validated_data["course"]
        }
    
    def pop_scooso_data(self, validated_data: dict) -> dict:
        return {
            "time_id": validated_data.pop("time_id"),
            "lesson_type": validated_data.pop("lesson_type"),
        }
