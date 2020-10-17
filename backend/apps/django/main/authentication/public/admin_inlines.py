from apps.django.utils.admins import DefaultAdminInlineMixin

from ..models import User

__all__ = [
    "UserAdminInline"
]


class UserAdminInline(DefaultAdminInlineMixin):
    model = User
    fieldset_fields = {
        "default": ["first_name", "last_name", "id", "!..."]
    }
