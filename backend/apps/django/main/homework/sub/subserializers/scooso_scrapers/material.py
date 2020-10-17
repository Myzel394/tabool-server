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
    
    def pop_scooso_data(self, validated_data: dict) -> dict:
        return {
            "scooso_id": validated_data.pop("scooso_id"),
            "owner_id": validated_data.pop("owner_id")
        }
    
    def rename_data(self, validated_data: dict) -> dict:
        return {
            "created_at": validated_data["created_at"],
            "lesson": validated_data["lesson"],
            "name": validated_data["filename"]
        }
