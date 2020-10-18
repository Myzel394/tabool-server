from apps.django.utils.serializers import WritableAllFieldMixin
from ..models import User

__all__ = [
    "UserField"
]


class UserField(WritableAllFieldMixin):
    model = User
