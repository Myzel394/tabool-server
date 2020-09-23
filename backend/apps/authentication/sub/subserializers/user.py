from rest_framework import serializers

from ...models import User

# TODO: Add field-level exceptions!


__all__ = [
    "UserDetailSerializer"
]


# TODO: Add password changer


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email", "first_name", "last_name", "password", "id"
        ]
        read_only_fields = ["id"]
