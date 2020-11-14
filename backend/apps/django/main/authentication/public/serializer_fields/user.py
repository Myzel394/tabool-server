from apps.django.main.authentication.models import User
from apps.django.main.authentication.sub.subserializers.user import UserDetailSerializer
from apps.django.utils.serializers import WritableAllFieldMixin

__all__ = [
    "UserField"
]


class UserField(WritableAllFieldMixin):
    model = User
    detail_serializer = UserDetailSerializer
