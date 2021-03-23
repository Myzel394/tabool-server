from rest_framework import serializers

from apps.django.utils.serializers import ScoosoScraperSerializerMixin
from ....models import Room, RoomScoosoData

__all__ = [
    "RoomScoosoScraperSerializer"
]


class RoomScoosoScraperSerializer(ScoosoScraperSerializerMixin):
    class Meta:
        model = Room
        scooso_model = RoomScoosoData
    
    code = serializers.CharField(required=False, allow_null=True)
    
    @staticmethod
    def constrain_place(given_place: str) -> str:
        if given_place.isdigit():
            return "0" * (3 - len(given_place)) + given_place
        return given_place
    
    def pop_scooso_data(self, validated_data: dict) -> dict:
        return {
            "scooso_id": validated_data.pop("scooso_id"),
            "code": validated_data["code"],
        }
    
    def rename_data(self, validated_data: dict) -> dict:
        return {
            "place": self.constrain_place(validated_data.pop("code")),
            **validated_data
        }
    
    def get_unique_data(self, validated_data: dict) -> dict:
        return {
            "place": validated_data["place"]
        }
