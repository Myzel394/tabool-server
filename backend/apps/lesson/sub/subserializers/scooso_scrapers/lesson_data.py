from rest_framework import serializers

from apps.utils.serializers.mixins import ScoosoScraperSerializerMixin
from constants.weekdays import ALLOWED_WEEKDAYS
from ....models import LessonData, LessonDataScoosoData

__all__ = [
    "LessonDataScoosoScraperSerializer"
]

ALLOWED_DAYS_NUMBERS = [x[0] for x in ALLOWED_WEEKDAYS]


class LessonDataScoosoScraperSerializer(ScoosoScraperSerializerMixin):
    class Meta:
        model = LessonData
        scooso_model = LessonDataScoosoData
    
    scooso_id = None
    lesson_type = serializers.UUIDField()
    
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    date = serializers.DateField()
    
    def pop_scooso_data(self, validated_data: dict) -> dict:
        return {
            "lesson_type": validated_data.pop("lesson_type"),
        }
    
    def get_unique_data(self, validated_data: dict) -> dict:
        return {
            "weekday": validated_data["date"].weekday(),
            "start_time": validated_data["start_time"],
            "end_time": validated_data["end_time"],
            "course": validated_data["course"]
        }
