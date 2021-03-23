from rest_framework import serializers

from apps.django.main.school_data.constants import SUBJECT_NAMES_MAPPING
from apps.django.utils.serializers import ScoosoScraperSerializerMixin
from ....models import Subject, SubjectScoosoData

__all__ = [
    "SubjectScoosoScraperSerializer"
]


class SubjectScoosoScraperSerializer(ScoosoScraperSerializerMixin):
    class Meta:
        model = Subject
        scooso_model = SubjectScoosoData
    
    code = serializers.CharField(required=False, allow_null=True)
    
    def pop_scooso_data(self, validated_data: dict) -> dict:
        return {
            "scooso_id": validated_data.pop("scooso_id"),
            "code": validated_data["code"],
        }
    
    def rename_data(self, validated_data: dict) -> dict:
        code: str = validated_data.pop("code").lower()
        name = SUBJECT_NAMES_MAPPING[code]
        
        return {
            "short_name": code,
            "name": name,
            **validated_data
        }
    
    def get_unique_data(self, validated_data: dict) -> dict:
        return {
            "short_name": validated_data["short_name"],
            "name": validated_data["name"]
        }
