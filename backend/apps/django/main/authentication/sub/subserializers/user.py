from rest_framework import serializers

from .preference import DetailPreferenceSerializer
from ...models import User

__all__ = [
    "UserInformationSerializer", "UserDetailSerializer", "UserUpdateSerializer"
]


class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "has_filled_out_data", "load_scooso_data", "preference", "is_confirmed", "first_name", "last_name",
            "email", "id"
        ]
    
    preference = serializers.SerializerMethodField()
    
    def get_preference(self, instance: User):
        return DetailPreferenceSerializer(instance=instance.preference, context=self.context).data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name"
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "load_scooso_data"
        ]
