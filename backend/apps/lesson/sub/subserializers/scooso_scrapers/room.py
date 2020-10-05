from rest_framework import serializers

from apps.lesson.models import Room, RoomScoosoData
from apps.utils.serializers.mixins import ScoosoScraperSerializerMixin

__all__ = [
    "RoomScoosoScraperSerializer"
]


class RoomScoosoScraperSerializer(ScoosoScraperSerializerMixin):
    class Meta:
        model = Room
        scooso_model = RoomScoosoData
    
    code = serializers.CharField()
    
    def pop_scooso_data(self, validated_data: dict) -> dict:
        return {
            "scooso_id": validated_data.pop("scooso_id"),
            "code": validated_data["code"],
        }
    
    def rename_data(self, validated_data: dict) -> dict:
        return {
            "place": validated_data.pop("code"),
            **validated_data
        }
