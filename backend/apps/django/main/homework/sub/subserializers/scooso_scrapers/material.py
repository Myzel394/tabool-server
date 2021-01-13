from rest_framework import serializers

from apps.django.utils.serializers import ScoosoScraperSerializerMixin
from ....models import Material, MaterialScoosoData

__all__ = [
    "MaterialScoosoScraperSerializer"
]


class MaterialScoosoScraperSerializer(ScoosoScraperSerializerMixin):
    class Meta:
        model = Material
        scooso_model = MaterialScoosoData
        fields = [
            "scooso_id", "owner_id", "filename", "created_at"
        ]
    
    scooso_id = serializers.IntegerField(min_value=0)
    owner_id = serializers.IntegerField(min_value=0)
    created_at = serializers.DateTimeField()
    filename = serializers.CharField()
    
    def get_unique_data(self, validated_data: dict) -> dict:
        return {
            "added_at": validated_data.pop("created_at"),
            "lesson": validated_data.pop("lesson"),
            "name": validated_data.pop("filename")
        }
    
    def pop_scooso_data(self, validated_data: dict) -> dict:
        return {
            "scooso_id": validated_data.pop("scooso_id"),
            "owner_id": validated_data.pop("owner_id")
        }
