from apps.utils.serializers import RandomIDSerializerMixin
from ...models import User

__all__ = [
    "UserDetailSerializer"
]


class UserDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = User
        fields = [
            "email", "first_name", "last_name", "password", "id"
        ]
