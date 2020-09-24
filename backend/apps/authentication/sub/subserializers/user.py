from rest_framework import serializers

from ...models import User

__all__ = [
    "UserDetailSerializer"
]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email", "first_name", "last_name", "password", "id"
        ]
