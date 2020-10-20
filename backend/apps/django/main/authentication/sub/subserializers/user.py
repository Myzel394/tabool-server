from rest_framework import serializers

from ...models import User

__all__ = [
    "UserInformationSerializer", "UserDetailSerializer"
]


class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email", "first_name", "last_name", "id"
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name"
        ]
