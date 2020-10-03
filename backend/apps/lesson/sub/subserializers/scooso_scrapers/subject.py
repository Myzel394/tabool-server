from rest_framework import serializers

from apps.utils.serializers.mixins import ScoosoSerializerMixin
from .... import constants
from ....models import Subject, SubjectScoosoData

__all__ = [
    "SubjectScoosoScraperSerializer"
]


class SubjectScoosoScraperSerializer(ScoosoSerializerMixin):
    class Meta:
        model = Subject
        scooso_model = SubjectScoosoData
    
    code = serializers.CharField()
    
    def pop_scooso_data(self, validated_data: dict) -> dict:
        return {
            "scooso_id": validated_data.pop("scooso_id"),
            "code": validated_data["code"],
        }
    
    def rename_data(self, validated_data: dict) -> dict:
        code = validated_data.pop("code")
        
        return {
            "short_name": code,
            "name": constants.SUBJECT_NAMES_MAPPING[code],
            "color": constants.SUBJECT_COLORS_MAPPING[code],
            **validated_data
        }
