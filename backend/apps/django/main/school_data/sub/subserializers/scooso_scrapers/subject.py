from rest_framework import serializers

from apps.django.extra.scooso_scraper.utils import rename_name_for_color_mapping
from apps.django.main.school_data.constants import SUBJECT_COLORS_MAPPING, SUBJECT_NAMES_MAPPING
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
        code = validated_data.pop("code")
        name = str(SUBJECT_NAMES_MAPPING[code])
        colors_mapping_name = rename_name_for_color_mapping(name)
        
        return {
            "short_name": code,
            "name": name,
            "color": SUBJECT_COLORS_MAPPING[colors_mapping_name],
            **validated_data
        }
    
    def get_unique_data(self, validated_data: dict) -> dict:
        return {
            "short_name": validated_data["short_name"],
            "name": validated_data["name"]
        }
