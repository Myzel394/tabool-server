from rest_framework import serializers

from apps.django.utils.serializers import ScoosoScraperSerializerMixin
from ....models import Teacher, TeacherScoosoData

__all__ = [
    "TeacherScoosoScraperSerializer"
]


class TeacherScoosoScraperSerializer(ScoosoScraperSerializerMixin):
    class Meta:
        model = Teacher
        scooso_model = TeacherScoosoData
    
    code = serializers.CharField()
    
    def pop_scooso_data(self, validated_data: dict) -> dict:
        return {
            "scooso_id": validated_data.pop("scooso_id"),
            "code": validated_data["code"],
        }
    
    def rename_data(self, validated_data: dict) -> dict:
        return {
            "short_name": validated_data.pop("code"),
            **validated_data
        }
    
    def get_unique_data(self, validated_data: dict) -> dict:
        return {
            "short_name": validated_data["short_name"]
        }
