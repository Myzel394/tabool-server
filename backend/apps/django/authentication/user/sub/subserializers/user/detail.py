from rest_framework import serializers

from .base import BaseUserSerializer

__all__ = [
    "DetailUserSerializer", "UserInformationSerializer"
]


class DetailUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "first_name", "last_name", "email", "id"
        ]


class UserInformationSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "preference", "first_name", "last_name", "email", "id", "user_type", "gender"
        ]
    
    preference = serializers.SerializerMethodField()
    
    def get_preference(self, instance: "User"):
        return instance.preference.data
