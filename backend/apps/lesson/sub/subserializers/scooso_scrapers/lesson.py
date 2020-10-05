from rest_framework import serializers

from apps.utils.serializers import ScoosoScraperSerializerMixin
from ....models import Lesson, LessonScoosoData

__all__ = [
    "LessonScoosoScraperSerializer"
]


class LessonScoosoScraperSerializer(ScoosoScraperSerializerMixin):
    class Meta:
        model = Lesson
        scooso_model = LessonScoosoData
        fields = [
            "time_id", "date"
        ]
    
    scooso_id = None
    time_id = serializers.IntegerField(min_value=0)
    
    date = serializers.DateField()
    
    def pop_scooso_data(self, validated_data: dict) -> dict:
        return {
            "time_id": validated_data.pop("time_id")
        }
